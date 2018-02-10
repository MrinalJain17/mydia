import numpy as np
from skvideo.io import FFmpegReader, ffprobe
from skvideo.utils import rgb2gray
from PIL import Image
from tqdm import tqdm


class Videos(object):
    """To read in videos and store them as NumPy arrays.

    The videos are stored as a 5-dimensional tensor - (<No. of Videos>, <No. of frames>, <height>, <width>, <channels>).
    The value of 'channels' could be 1 (gray scale) or 3 (RGB).

    Args:
        target_size (tuple): (New_Width, New_Height). Defaults to None.
            A tuple denoting the target width and height (of the frames) of the videos.
            If not set, the dimensions of the frames will not be altered.

            Note:
            A single video is a stack of frames. If the dimension of all the frames is not the same, they cannot by stacked.

        to_gray (boolean): Whether to convert each video (all the frames) to gray scale or not. Defaults to False.

        max_frames (int): The (maximum) number of frames to extract from each video. Defaults to None.
            Frames are extracted based on the value of 'extract_frames'.
            If not set, all the frames would be kept.

            Note:
            Videos are stacked together. If the number of frames in all the videos are not the same, they cannot be stacked.

        extract_frames (str): {'first', 'middle', 'last'}. Defaults to 'middle'.
            'first': Extract the frames from the beginning of the video.
            'last': Extract the frames from the end of the video.
            'middle': Extract the frames from the middle of the video.
                Removes ((total frames - 'max_frames') // 2) from the beginning ant the end of the video.

        required_fps (int): The number of frame(s) to capture per second from the video. Defaults to None.
            For each second of the video, only the first 'N' frames are captured.

            If set to 0, then the value of this parameter is adaptive to each video.
            It will extract exactly 'max_frames' frames from each of the video (of any duration).

            e.g. Let the duration of a video to be 10 seconds assume it was captured at the rate of 30fps.
            Suppose the value of 'required_fps' is set to 7.
            Then, for each second, the first 7 frames would be captured. The resulting video (in form of tensor) will have a total of 10*7=70 frames.

        normalize_pixels (tuple, str): Whether to normalize pixel values for each video or not. Defaults to None.
            tuple - (New_min, New_max): Min-max normalization will be used.
            str - 'z-score': Z-score normalization will be used.
            If not set, then the pixels would not be normalized.

            The pixel values would be normalized based on the pixels of each video.

    """

    def __init__(self, target_size=None, to_gray=False, max_frames=None,
                 extract_frames='middle', required_fps=None,
                 normalize_pixels=None):
        """Initializing the variables"""

        self.target_size = target_size
        self.to_gray = to_gray
        self.max_frames = max_frames
        self.extract_frames = extract_frames
        self.required_fps = required_fps
        self.normalize_pixels = normalize_pixels
        self.fps = None

    def read_videos(self, paths):
        """Function to read videos.

        Args:
            paths (list of str): A list of paths of the videos to be read.

        Returns:
            Numpy.ndarray: A 5-dimensional tensor with shape (<No. of Videos>, <No. of frames>, <height>, <width>, <channels>).
            The value of 'channels' could be 1 (gray scale) or 3 (RGB).

        Raises:
            ValueError: If the value of 'normalize_pixels' is invalid.

        """

        list_of_videos = [
            self._read_video(path) for path in tqdm(paths)
        ]

        tensor = np.vstack(list_of_videos)

        if self.normalize_pixels is not None:
            # Pixels are normalized for each video individually
            if (isinstance(self.normalize_pixels, tuple)) and (
                    len(self.normalize_pixels) == 2):
                base = self.normalize_pixels[0]
                r = self.normalize_pixels[1] - base
                min_ = np.min(tensor, axis=(1, 2, 3), keepdims=True)
                max_ = np.max(tensor, axis=(1, 2, 3), keepdims=True)
                return ((tensor.astype('float32') - min_) /
                        (max_ - min_)) * r + base

            elif self.normalize_pixels == 'z-score':
                mean = np.mean(tensor, axis=(1, 2, 3), keepdims=True)
                std = np.std(tensor, axis=(1, 2, 3), keepdims=True)
                return (tensor.astype('float32') - mean) / std

            else:
                raise ValueError('Invalid value of \'normalize_pixels\'')

        return tensor

    def get_frame_count(self, paths):
        """Get the number of frames of all the videos.

        Can be used to determine the value of 'max_frames'.

        Args:
            paths (list of str): A list of paths of the videos to be read.

        Returns:
            dict (python dictionary): Key - path of video, value - number of frames in that video.

        """

        frame_count = {}
        for path in paths:
            cap = FFmpegReader(filename=path)
            frame_count[path] = cap.inputframenum
            cap.close()

        return frame_count

    def _read_video(self, path):
        """Used internally by 'read_videos()' to read in a single video.

        Args:
            path (str): Path of the video to be read.

        Returns:
            Numpy.ndarray: A 5-dimensional tensor with shape (1, <No. of frames>, <height>, <width>, <channels>).
            The value of 'channels' could be 1 (gray scale) or 3 (RGB).

        """

        cap = FFmpegReader(filename=path)
        list_of_frames = []
        self.fps = int(cap.inputfps)                  # Frame Rate

        for index, frame in enumerate(cap.nextFrame()):

            capture_frame = True
            if self.required_fps is not None:
                curr_required_fps = self.required_fps

                # Adaptive selection of frames
                if self.required_fps == 0:
                    frame_count = cap.inputframenum
                    duration = frame_count / self.fps
                    curr_required_fps = int(
                        np.ceil(self.max_frames / duration))

                is_valid = range(curr_required_fps)
                capture_frame = (index % self.fps) in is_valid

            if capture_frame:

                if self.target_size is not None:
                    temp_image = Image.fromarray(frame)
                    frame = np.asarray(
                        temp_image.resize(
                            self.target_size,
                            Image.ANTIALIAS)).astype('uint8')

                # Shape of each frame -> (<height>, <width>, 3)
                list_of_frames.append(frame)

        temp_video = np.stack(list_of_frames)
        cap.close()

        if self.to_gray:
            temp_video = rgb2gray(temp_video)

        if self.max_frames is not None:
            temp_video = self._process_video(video=temp_video)

        return np.expand_dims(temp_video, axis=0)

    def _process_video(self, video):
        """Used internally by '_read_video()' to extract the required frames.

        Args:
            video (Numpy.ndarray): A tensor of shape (<No. of frames>, <height>, <width>, <channels>).
                The tensor is the video whose frames are to be extracted.

        Returns:
            Numpy.ndarray: A tensor (processed video) with shape (<`max_frames`>, <height>, <width>, <channels>).

        Raises:
            ValueError: If the value of 'extract_frames' is invalid.
            IndexError: If the required number of frames is greater than the total number of frames in the video.

        """

        total_frames = video.shape[0]
        if self.max_frames <= total_frames:

            if self.extract_frames == 'first':
                video = video[:self.max_frames]
            elif self.extract_frames == 'last':
                video = video[(total_frames - self.max_frames):]
            elif self.extract_frames == 'middle':
                # No. of frames to remove from the front
                front = ((total_frames - self.max_frames) // 2) + 1
                video = video[front:(front + self.max_frames)]
            else:
                raise ValueError('Invalid value of \'extract_frames\'')

        else:
            raise IndexError(
                'Required number of frames is greater than the total number of frames in the video')

        return video
