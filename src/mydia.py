import warnings

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skvideo.io import FFmpegReader, ffprobe
from skvideo.utils import rgb2gray
from tqdm import tqdm


class Videos(object):
    """

    """

    def __init__(
        self,
        target_size=None,
        to_gray=False,
        mode="auto",
        num_frames=None,
        extract_position="first",
        required_fps=None,
        normalize=None,
        random_state=17,
    ):
        """

        """

        self.target_size = None
        if (target_size != None):
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
        self.random_state = random_state
        np.random.seed(self.random_state)

    def _read_video(self, path):
        """

        """

        cap = FFmpegReader(filename=path)
        fps = int(cap.inputfps)
        total_frames = cap.inputframenum
        if self.target_size == None:
            width, height = (cap.inputwidth, cap.inputheight)
        else:
            width, height = self.target_size

        if (self.num_frames == None) and (self.required_fps == None):
            self.num_frames = total_frames
            indices = np.arange(total_frames, dtype=np.int)
        else:
            if self.required_fps > fps:
                raise IndexError(
                    "The value of 'required_fps' is greater than the `fps` value of the video."
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
        """

        """

        if self.mode == "auto":
            indices = np.linspace(
                0, kwargs["total_frames"], self.num_frames, endpoint=True, dtype=np.int
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
        """

        """

        total_frames = len(index_array)
        if self.num_frames < total_frames:
            if self.extract_position == "first":
                return index_array[:self.num_frames]

            elif self.extract_position == "last":
                return index_array[(total_frames - self.num_frames):]

            elif self.extract_position == "middle":
                front = (
                    (total_frames - self.num_frames) // 2
                ) + 1  # No. of frames to remove from the front
                return index_array[front:(front + self.num_frames)]

        else:
            raise IndexError(
                "The value of 'num_frames' is greater than the total number of frames available."
            )

    def read(self, paths):
        """

        """

        list_of_videos = [self._read_video(path) for path in tqdm(paths, unit="videos")]
        video_tensor = np.vstack(list_of_videos)

        if self.normalize != None:
            pass

        return video_tensor
