import warnings

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skvideo.io import FFmpegReader
from skvideo.utils import rgb2gray
from tqdm import tqdm


class Videos(object):
    """To read in videos and store them as NumPy arrays.

    The videos are stored as a 5-dimensional tensor with shape:  
    
    `(<No. of Videos>, <No. of frames>, <height>, <width>, <channels>)` - if `data_format` is set to "channels_last" or,  
    `(<No. of Videos>, <channels>, <No. of frames>, <height>, <width>)` - if `data_format` is set to "channels_first".

    The value of `channels` could be 1 (gray scale) or 3 (RGB).

    Parameters
    ----------
    target_size : tuple, optional
        Tuple of form `(New_Width, New_Height)`, defaults to `None`.  
        A tuple denoting the target width and height (of the frames) of the videos. 
        If not set, the dimensions of the frames will not be altered.  
        
        Note:  
        A single video is a stack of frames. If the dimension of all the frames is not the same, they cannot by stacked.
    
    to_gray : bool, optional
        If `True`, all the frames of the videos are converted to gray scale, defaults to `False`.
    
    mode : str, optional
        One of {"auto", "manual", "random"}, defaults to `auto`.  
        
        `auto`: The reader will read frames at equal intervals from the entire video. 
        The number of frames to be extracted (read) will depend on the value of `num_frames`.  
        `manual`: The user would manually provide the details to extract frames from the video. 
        Available parameters to tune are `num_frames`, `extract_position` and `required_fps`.  
        `random`: The reader will read frames at random from the entire video. 
        The number of frames to be extracted (read) will depend on the value of `num_frames`.
    
    num_frames : int, optional
        The (exact) number of frames to extract from each video, defaults to `None`.  
        Frames are extracted based on the value of `mode`.  
        If set to `None`, all the frames of the video would be kept.

        Note:  
        Videos are stacked together. If the number of frames in all the videos are not the same, they cannot be stacked.
    
    extract_position : str, optional
        One of {"first", "middle", "last"}, defaults to `first`.  
        
        `first`: Extract the frames from the beginning of the video.  
        `last`: Extract the frames from the end of the video.  
        `middle`: Extract the frames from the middle of the video  
        (Removes `(total frames - 'max_frames') // 2` from the beginning as well as the end of the video)
    
    required_fps : int, optional
        The number of frame(s) to capture per second from the video, defaults to `None`.  
        
        Example:  
        Let the duration of a video to be 10 seconds and assume that it was captured at the rate of 30fps.  
        Suppose the value of `required_fps` is set to 7.  
        Then for each second, the **first** 7 frames would be captured.  
        The resulting video (in form of tensor) will have a total of 10 x 7 = 70 frames.
    
    normalize : bool, optional
        If `True`, then the pixel values will be normalized to be in range (0, 1), defaults to `False`.  

    data_format : str
        One of {"channels_first", "channels_last"}, defaults to `channels_last`.

        `channels_last` corresponds to the tensors with the following dimension - 
        `(<No. of Videos>, <No. of frames>, <height>, <width>, <channels>)`

         `channels_first` corresponds to the tensors with the following dimension - 
        `(<No. of Videos>, <channels>, <No. of frames>, <height>, <width>)`

        Use `channels_last` when using libraries like *tensorflow/keras* and `channels_first` when working 
        with *pytorch* or *theano*.
    
    random_state : int, optional
        The number to seed the random number generator (when using the `mode` as "random"), defaults to 17.

    """

    def __init__(
        self,
        target_size=None,
        to_gray=False,
        mode="auto",
        num_frames=None,
        extract_position="first",
        required_fps=None,
        normalize=False,
        data_format="channels_last",
        random_state=17,
    ):
        """Initializing class variables

        """

        self.target_size = None
        if target_size != None:
            if isinstance(target_size, int):
                self.target_size = (target_size, target_size)
            elif len(target_size) == 2:
                self.target_size = target_size
            else:
                raise ValueError("Invalid value of 'target_size'")

        self.to_gray = to_gray
        if mode in ["auto", "manual", "random"]:
            self.mode = mode
        else:
            raise ValueError("Invald value of 'mode'")

        self.num_frames = num_frames
        if extract_position in ["first", "middle", "last"]:
            self.extract_position = extract_position
        else:
            raise ValueError("Invalid value of 'extract_position'")

        self.required_fps = 0
        if required_fps != None:
            self.required_fps = int(required_fps)
            if num_frames == None:
                warnings.warn(
                    "Set a value for 'num_frames' to avoid unexpected behaviour"
                )
        self.normalize = normalize
        if data_format in ["channels_last", "channels_first"]:
            self.data_format = data_format
        else:
            raise ValueError("Invalid value of 'data_format'")
        self.random_state = random_state
        np.random.seed(self.random_state)

    def _read_video(self, path):
        """Used internally by `read()` to read in a single video.

        Parameters
        ----------
        path : str
            Path of the video to be read.
        
        Returns
        -------
        numpy.ndarray
            A 5-dimensional tensor - the shape of which will depend on the value of `data_format`  

        """

        cap = FFmpegReader(filename=path)
        fps = int(cap.inputfps)
        total_frames = cap.inputframenum
        if self.target_size == None:
            width, height = (cap.inputwidth, cap.inputheight)
        else:
            width, height = self.target_size

        if (self.num_frames == None) and (self.required_fps == 0):
            self.num_frames = total_frames
            indices = np.arange(total_frames, dtype=np.int)
        else:
            if self.required_fps > fps:
                raise IndexError(
                    "The value of 'required_fps' is greater than the `fps` value of the video"
                )

            indices = self._get_frame_indices(total_frames=total_frames, fps=fps)

        video = np.zeros((self.num_frames, height, width, 3), dtype=np.int)
        vid_index = 0

        for idx, frame in enumerate(cap.nextFrame()):
            if idx in indices:
                if self.target_size != None:
                    image = Image.fromarray(frame)
                    image = image.resize((width, height), resample=Image.ANTIALIAS)
                    frame = np.asarray(image, dtype="uint8")

                video[vid_index, :, :, :] = frame
                vid_index += 1

        cap.close()

        if self.to_gray:
            video = rgb2gray(video)

        return np.expand_dims(video, axis=0)

    def _get_frame_indices(self, **kwargs):
        """Used internally by `_read_video()` to get an array to indices to extract the frames.

        """

        if self.mode == "auto":
            indices = np.linspace(
                0, kwargs["total_frames"], self.num_frames, endpoint=False, dtype=np.int
            )
        elif self.mode == "manual":
            if self.required_fps > 0:
                indices_list = []
                for i in range(kwargs["total_frames"]):
                    if (i % kwargs["fps"]) in range(self.required_fps):
                        indices_list.append(i)
                indices = np.array(indices_list)
            else:
                indices = np.arange(kwargs["total_frames"])
            indices = self._remove_extra_frames(indices)
        elif self.mode == "random":
            indices = np.random.randint(
                0, kwargs["total_frames"] + 1, self.num_frames, dtype=np.int
            )

        return indices

    def _remove_extra_frames(self, index_array):
        """Used internally by `_read_video()` to crop out extra frames from the video.

        """

        total_frames = len(index_array)
        if self.num_frames < total_frames:
            if self.extract_position == "first":
                return index_array[: self.num_frames]

            elif self.extract_position == "last":
                return index_array[(total_frames - self.num_frames) :]

            elif self.extract_position == "middle":
                front = (
                    (total_frames - self.num_frames) // 2
                ) + 1  # No. of frames to remove from the front
                return index_array[front : (front + self.num_frames)]

        else:
            raise IndexError(
                "The value of 'num_frames' is greater than the total number of frames available"
            )

    def read(self, paths):
        """Function to read videos.

        Parameters
        ----------
        paths : list
            A list of paths of the videos to be read.
        
        Returns
        -------
        numpy.ndarray
            A 5-dimensional tensor - the shape of which will depend on the value of `data_format`  

        """

        if not isinstance(paths, list):
            if isinstance(paths, str):
                paths = [paths]
            else:
                raise ValueError("Invalid value of 'paths'")

        list_of_videos = [self._read_video(path) for path in tqdm(paths, unit="videos")]
        video_tensor = np.vstack(list_of_videos)

        if self.data_format == "channels_first":
            video_tensor = np.transpose(video_tensor, axes=(0, 4, 1, 2, 3))

        if self.normalize:
            video_tensor = video_tensor.astype(np.float) / 255

        return video_tensor

    def plot(self, video=None, path=None, num_col=3, figsize=None):
        """Plot the frames of the video in a grid.

        Parameters
        ----------
        video : numpy.ndarray
            A video tensor with shape `(<No. of frames>, <height>, <width>, <channels>)` or 
            `(<channels>, <No. of frames>, <height>, <width>)`, depending on the value of `data_format`.
        
        path : str
            The path of the video to be plotted.  
            Either pass the path of the video, or the video itself.  
            If both are passed, the one for which the path is provided will be used.
        
        num_col : int, optional
            The number of columns the grid should have, defaults to 3.
        
        figsize : tuple, optional
            The size of the entire figure, defaults to `None`.  
            This tuple is passes to the `matplotlib.figure` object to set it's size.  
            If set as `None`, it is calculated automatically (recommended).

        """

        if not isinstance(video, type(None)):
            if video.ndim != 4:
                raise ValueError("Invalid value for 'video'")

        elif path != None:
            video = self.read(path)[0]
        else:
            raise ValueError("Either pass a 'video' or a 'path' to the video")

        if not ((video.shape[-1] == 1) or (video.shape[-1] == 3)):
            # If the channels are not at the end, they should be at the beginning
            video = np.transpose(video, axes=(1, 2, 3, 0))

        gray = True if video.shape[-1] == 1 else False

        num_row = int(np.ceil(video.shape[0] / num_col))
        if figsize == None:
            figsize = (7 * num_col, 4 * num_row)  # Based on trails and errors
        else:
            if isinstance(figsize, int):
                figsize = (figsize, figsize)
            elif len(figsize) != 2:
                raise ValueError("Invalid value for 'figsize'")

        fig = plt.figure(figsize=figsize)
        for index, frame in enumerate(video):
            if index != 0:  # Shows the axis only for the first frame
                ax = fig.add_subplot(num_row, num_col, index + 1, xticks=[], yticks=[])
            else:
                ax = fig.add_subplot(num_row, num_col, index + 1)
            if gray:
                ax.imshow(np.squeeze(frame), cmap="gray")
            else:
                ax.imshow(frame)
