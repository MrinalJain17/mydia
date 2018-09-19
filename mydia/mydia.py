"""Mydia: Read videos as numpy arrays

The class `Videos` in this module can be used to read videos with advance support
for frame selection, frame resizing and normalization.

The module is a wrapper around the library `ffmpeg-python`, and uses `FFmpeg` as 
its backend to process the videos.

"""

__version__ = "2.0.0"
__author__ = "Mrinal Jain"

import warnings
from typing import List, Tuple, Union

import ffmpeg
import numpy as np
from tqdm import tqdm

from .utils import (
    TargetSize,
    _mode_auto,
    _mode_first,
    _mode_last,
    _mode_middle,
    _mode_random,
)

NUM_CHANNELS = {"rgb24": 3, "gray": 1}
MODES = {
    "auto": _mode_auto,
    "random": _mode_random,
    "first": _mode_first,
    "last": _mode_last,
    "middle": _mode_middle,
}


class Videos(object):
    """Class to read in videos and store them as numpy arrays

    The videos are stored as a 5-dimensional tensor where the shape of the tensor depends on the `data_format`.

    If the `data format`="channels_last"` => :code:`(<num_videos>, <num_frames>, <height>, <width>, <channels>)`

    If the `data format`="channels_first"` => :code:`(<num_videos>, <channels>, <num_frames>, <height>, <width>)`

    The value of `channels` will be 1 (for gray scale) or 3 (for RGB).

    Args:
        target_size: Tuple of form `(new_width, new_height)`, defaults to None
            If not set, the dimensions of the frames will not be altered
        to_gray: 
            If True, all the frames of the video(s) are converted to gray scale, defaults to False
        mode: One of {"auto", "random", "first", "last", "middle"}, defaults to `auto`
            :code:`auto`: The reader will read `num_frames` frames at equal intervals from the entire video
            
            :code:`random`: The reader will read `num_frames` frames at random from the entire video
            
            :code:`first`: The reader will read the first `num_frames` frames

            :code:`last`: The reader will read the last `num_frames` frames

            :code:`middle`: The reader will read the middle `num_frames` frames, by removing equal number of
            frames from the beginning and end of the video
        num_frames: The (exact) number of frames to extract from each video, defaults to None
            Frames are extracted based on the value of :code:`mode`. 
            If set to None, all the frames of the video would be kept.
        normalize: 
            If True, then the pixel values will be normalized to be in range `(0, 1)`, defaults to False.
        data_format: One of {"channels_first", "channels_last"}, defaults to `channels_last`.
            Use `channels_last` when using libraries like **tensorflow/keras** and `channels_first` when working 
            with **pytorch** or **theano**.
        random_state:
            The number to seed the random number generator (when using the `mode` as "random"), defaults to 17.

    Example::

        from mydia import Videos

        reader = Videos(target_size=(720, 480),
                        to_gray=False,
                        num_frames=128,
                        data_format="channels_first")

        video = reader.read('/path/to/video')

    """

    def __init__(
        self,
        target_size: Tuple[int, int] = None,
        to_gray: bool = False,
        mode: str = "auto",
        num_frames: int = None,
        normalize: bool = False,
        data_format: str = "channels_last",
        random_state: int = 17,
    ) -> None:
        """Initializing class variables"""

        self.target_size = None
        if target_size is not None:
            if isinstance(target_size, tuple) and len(target_size) == 2:
                self.target_size = TargetSize(
                    width=target_size[0], height=target_size[1], rescale=True
                )
            else:
                raise ValueError("Invalid value of 'target_size'")

        self.pix_fmt = "rgb24"
        if to_gray:
            self.pix_fmt = "gray"

        if isinstance(mode, str):
            if mode in ["auto", "first", "middle", "last", "random"]:
                self.mode = MODES[mode]
            else:
                raise ValueError("Invald value of 'mode'")
        else:
            self.mode = mode

        self.num_frames = num_frames
        self.normalize = normalize

        if data_format in ["channels_last", "channels_first"]:
            self.data_format = data_format
        else:
            raise ValueError("Invalid value of 'data_format'")

        np.random.seed(random_state)

    def _read_video(self, path: str) -> np.ndarray:
        """Used internally by :code:`read()` to read in a single video.

        Args:
            path: Path of the video to be read

        Returns:
            A 5-dimensional tensor - the shape of which will depend on the value of :code:`data_format`

        """

        fps, total_frames = self._probe(path)
        width = self.target_size.width
        height = self.target_size.height

        out = ffmpeg.input(filename=path)
        if self.num_frames is not None:
            if self.num_frames <= total_frames:
                indices = self.mode(total_frames, self.num_frames, fps)
                select_str = "+".join([f"eq(n,{idx})" for idx in indices])
                out = out.filter("select", select_str)
            else:
                raise IndexError(
                    "The value of 'num_frames' is greater than the total number "
                    "of frames available"
                )
        if self.target_size.rescale:
            out = out.filter("scale", width, height)
        out = out.output("pipe:", vsync=0, format="rawvideo", pix_fmt=self.pix_fmt)
        out = out.global_args("-loglevel", "panic", "-hide_banner")
        out, _ = out.run(capture_stdout=True)

        video = np.frombuffer(out, np.uint8).reshape(
            [-1, height, width, NUM_CHANNELS[self.pix_fmt]]
        )

        return np.expand_dims(video, axis=0)

    def _probe(self, path: str) -> Tuple[int, int]:
        """Used internally by :code:`_read_video()` to get the meta-data of a video"""

        probe = ffmpeg.probe(filename=path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )

        # If the frame rate is 25, then the 'avg_frame_rate' is of the form `25/1`
        fps = int(video_stream["avg_frame_rate"].split("/")[0])
        total_frames = int(video_stream["nb_frames"])
        if self.target_size is None:
            self.target_size = TargetSize(
                width=video_stream["width"], height=video_stream["height"]
            )

        return (fps, total_frames)

    def read(self, paths: Union[str, List[str]]) -> np.ndarray:
        """Function to read videos

        Args:
            paths: A list of paths of the videos to be read.
        
        Returns:
            A 5-dimensional tensor - the shape of which will depend on the value of :code:`data_format`
        
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


def plot(video: np.ndarray, num_col: int = 3, figsize: Tuple[int, int] = None) -> None:
    """Plot the frames of the video in a grid

    Args:
        video: 
            A video tensor with shape :code:`(<num_frames>, <height>, <width>, <channels>)` or 
            :code:`(<channels>, <num_frames>, <height>, <width>)`, depending on the value of `data_format`
        num_col: 
            The number of columns the grid should have, defaults to 3
        figsize: The size of the matplotlib figure, defaults to None
            This tuple is passed to the `matplotlib.figure` object to set it's size

            If set as None, it is calculated automatically (recommended)
    
    """

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise (
            "ImportError: 'matplotlib', required to plot the video frames, cannot be imported"
        )

    if video.ndim != 4:
        raise ValueError("Invalid value for 'video'")

    # If the channels are not at the end, then the format of the video is `channels_first`
    # which needs to be converted to `channels_last`
    if not ((video.shape[-1] == 1) or (video.shape[-1] == 3)):
        video = np.transpose(video, axes=(1, 2, 3, 0))

    gray = True if video.shape[-1] == 1 else False

    num_row = int(np.ceil(video.shape[0] / num_col))
    if figsize is None:
        figsize = (7 * num_col, 4 * num_row)  # Based on trails and errors
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
