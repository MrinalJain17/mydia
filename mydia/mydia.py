"""Mydia: A simple and efficient wrapper for reading videos as NumPy tensors

The class :class:`Videos` in this module can be used to read videos with advance support 
for frame selection, frame resizing, pixel normalization and grayscale conversion.

The module  uses **FFmpeg** as its backend to process the videos.

"""

__version__ = "2.1.1"
__author__ = "Mrinal Jain"

import warnings
from typing import NamedTuple

import ffmpeg
import numpy as np
from tqdm import tqdm

from .utils import _mode_auto, _mode_first, _mode_last, _mode_middle, _mode_random

NUM_CHANNELS = {"rgb24": 3, "gray": 1}
MODES = {
    "auto": _mode_auto,
    "random": _mode_random,
    "first": _mode_first,
    "last": _mode_last,
    "middle": _mode_middle,
}


class TargetSize(NamedTuple):
    """A named tuple representing tha target size of frames of a video"""

    width: int
    height: int
    rescale: bool = False


class Videos(object):
    """Class to read in videos and store them as numpy arrays

    The videos are stored as a 5-dimensional tensor where the shape of the tensor depends 
    on the ``data_format``.

    :param target_size: 
        A tuple of form ``(width, height)`` indicating the dimension to resize the frames 
        of the video, defaults to `None`. The dimension of the frames will not be altered 
        if this parameter is not set.
    :type target_size: tuple[int, int]

    :param to_gray: Convert video to grayscale, defaults to `False`.
    :type to_gray: bool

    :param num_frames: 
        The (exact) number of frames to extract from the video, defaults to `None`. Frames 
        are extracted based on the value of ``mode``. If not set, all the frames of the 
        video are kept.
    :type num_frames: int

    :param mode: 
        The method used for frame extraction, if ``num_frames`` is set. It could be one 
        of "auto", "random", "first", "last" or "middle". 

        * ``"auto"``: **N** frames will be extracted at equal intervals
        * ``"random"``: **N** frames will be randomly extracted (no repetetion). Set the 
          parameter `random_state` to get the same result every time.
        * ``"first"``, ``"last"`` and ``"middle"`` will extract **N** contiguous frames 
          from the beginning, end and middle of the video respectively.

    :type mode: str

    :param normalize: 
        Shifts each video to the range `(0, 1)` by subtracting the minimum and dividing by 
        the difference between the maximum and the minimum pixel value. Defaults to `False`
    :type normalize: bool

    :param data_format: 
        Video data format, either "channels_last" or "channels_first". 
        
        * ``"channels_last"``: The tensor will have shape 
          ``(<samples>, <frames>, <height>, <width>, <channels>)``
        * ``"channels_first"``: The tensor will have shape 
          ``(<samples>, <channels>, <frames>, <height>, <width>)``
        
        ``channels`` will be **1** for grayscale videos and **3** for RGB videos.
    :type data_format: str

    :param random_state: 
        Integer that seeds the (numpy) random number generator, defaults to 17.
    :type random_state: int

    **Example**

    .. code-block:: python

       from mydia import Videos
   
       reader = Videos(
           target_size=(720, 480),
           to_gray=False,
           num_frames=128,
           data_format="channels_first"
       )
   
       video = reader.read("./path/to/video")

    .. note::

       .. versionchanged:: 2.0.0
   
          You could also pass a `callable` to ``mode`` for custom frame extraction. The 
          `callable` should return a **list of integers**, denoting the indices of the 
          frames to be extracted. It should take 3 (non-keyword) arguments: 
   
          * ``total_frames``: The total number of frames in the video
          * ``num_frames``: The number of frames that you want to extract
          * ``fps``: The frame rate of the video
   
          These arguments may/may not be used to generate the required frame indices. 
          Detailed examples are provided in the documentation.

          .. warning::
      
             If you are passing a `callable` to ``mode``, then make sure that the number 
             of frames (indices) it returns is equal to the value of ``num_frames``. If 
             this condition is not met, then this would mean that the number of frames 
             selected is different for different videos, and therefore they cannot be 
             stacked into a single tensor.

    """

    def __init__(
        self,
        target_size=None,
        to_gray=False,
        num_frames=None,
        mode="auto",
        normalize=False,
        data_format="channels_last",
        random_state=17,
    ):
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

        self.num_frames = num_frames

        if isinstance(mode, str):
            if mode in ["auto", "first", "middle", "last", "random"]:
                self.mode = MODES[mode]
            else:
                raise ValueError("Invald value of 'mode'")
        else:
            self.mode = mode

        self.normalize = normalize

        if data_format in ["channels_last", "channels_first"]:
            self.data_format = data_format
        else:
            raise ValueError("Invalid value of 'data_format'")

        np.random.seed(random_state)

    def _read_video(self, path):
        """Used internally by :func:`read()` to read in a **single** video.

        :param path: The path of the video to be read.
        :type path: str

        :return:
            A 5-dimensional tensor, whose shape will depend on the value of ``data_format``

            * For ``"channels_last"``: The tensor will have shape 
              ``(1, <frames>, <height>, <width>, <channels>)``
            * For ``"channels_first"``: The tensor will have shape 
              ``(1, <channels>, <frames>, <height>, <width>)``

        :rtype: :obj:`numpy.ndarray`

        """

        fps, total_frames = self._probe(path)
        width = self.target_size.width
        height = self.target_size.height

        out = ffmpeg.input(filename=path)

        if self.num_frames is not None:
            if self.num_frames <= total_frames:
                indices = self.mode(total_frames, self.num_frames, fps)
                temp_msg = """The number of frames to be selected returned by the callable 
                does not match the value of the parameter 'num_frames'. Your callable 
                should return the same number of frames for every video, regardless of their 
                individual duration."""
                assert len(indices) == self.num_frames, temp_msg
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

        if self.normalize:
            min_, max_ = np.min(video), np.max(video)
            video = np.clip(video, min_, max_)
            video = (video.astype("float") - min_) / (max_ - min_ + 1e-5)

        return np.expand_dims(video, axis=0)

    def _probe(self, path):
        """Used internally by :func:`_read_video()` to get the meta-data of a video

        .. note::

           This function also sets the `default` dimensions of the video, if the frames 
           are not to be resized.

        :param path: The path of the video to be read.
        :type path: str

        :return: Frame rate and total number of frames in the video.
        :rtype: tuple[int, int]

        """

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

    def read(self, paths, verbose=1):
        """Function to read videos

        :param paths: A list of paths/path of the video(s) to be read.
        :type paths: str or list[str]

        :param verbose: If set to 0, the progress bar will be disabled.
        :type verbose: int
        
        :return: 
            A 5-dimensional tensor, whose shape will depend on the value of ``data_format``.
            
            * For ``"channels_last"``: The tensor will have shape 
              ``(<samples>, <frames>, <height>, <width>, <channels>)``
            * For ``"channels_first"``: The tensor will have shape 
              ``(<samples>, <channels>, <frames>, <height>, <width>)``

        :rtype: :obj:`numpy.ndarray`

        :raises ValueError: If ``paths`` is neither a string, not a list of strings.
        :raises IndexError: 
            If ``num_frames`` is set to a value greater than the total number of frames 
            available in the video.

        .. important::

           If multiple videos are to be read, then each video should have the same dimension 
           ``(frames, height, width)``, otherwise they cannot be stacked into a single 
           tensor. Therefore, the user **must** use the parameters ``target_size`` and 
           ``num_frames`` to make sure of this.
        
        """

        if not isinstance(paths, list):
            if isinstance(paths, str):
                paths = [paths]
            else:
                raise ValueError("Invalid value of 'paths'")
        disable = False
        if verbose == 0:
            disable = True

        list_of_videos = [
            self._read_video(path)
            for path in tqdm(paths, unit="videos", disable=disable)
        ]
        video_tensor = np.vstack(list_of_videos)

        if self.data_format == "channels_first":
            video_tensor = np.transpose(video_tensor, axes=(0, 4, 1, 2, 3))

        return video_tensor


def plot(video, num_col=3, figsize=None):
    """Plot the frames of the video in a grid

    :param video: A 5-dimensional video tensor. 
    :type video: :obj:`numpy.ndarray` 

    :param num_col: The number of columns in the grid, defaults to 3.
    :type num_col: int

    :param figsize: 
        The size of the matplotlib figure, defaults to `None`. This tuple is passed to the 
        ``matplotlib.figure`` object to set it's size. If set as `None`, it is calculated 
        automatically (recommended).
    :type figsize: tuple[int, int] 

    :raises ImportError: If ``matplotlib`` is not successfully imported.
    :raises ValueError: If the dimension of the ``video`` tensor is invalid.
    
    """

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ("ImportError: Unable to import 'matplotlib' for plotting video frames")

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
