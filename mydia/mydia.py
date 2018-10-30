"""Mydia: A simple and efficient wrapper for reading videos as NumPy tensors

The class :class:`Videos` in this module can be used to read videos with 
advance support for frame selection, frame resizing, pixel normalization 
and grayscale conversion.

The module  uses **FFmpeg** as its backend to read and process the videos.

"""

__version__ = "2.2.0.4"
__author__ = "Mrinal Jain"

import warnings
from multiprocessing import Pool, cpu_count
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

    The videos are stored as a 5-dimensional tensor where the shape of 
    the tensor depends on ``data_format``.

    Parameters
    ----------
    target_size : tuple[int, int]
        A tuple of form ``(width, height)`` indicating the dimension to 
        resize the frames of the video, defaults to `None`. The dimension 
        of the frames will not be altered if this parameter is not set.
    to_gray : bool
        Convert video to grayscale, defaults to `False`.
    num_frames : int
        The (exact) number of frames to extract from the video, defaults 
        to `None`. Frames are extracted based on the value of ``mode``. 
        If not set, all the frames of the video are kept.
    mode : str
        The method used for frame extraction if ``num_frames`` is set. 
        It could be one of "auto", "random", "first", "last" or "middle".

        * ``"auto"``: **N** frames will be extracted at equal intervals.
        * ``"random"``: **N** frames will be randomly extracted (no 
          repetetion). Use ``random_state`` to ensure reproducibility.
        * ``"first"``, ``"last"`` and ``"middle"`` will extract **N** 
          contiguous frames from the beginning, end and middle of the 
          video respectively.
    normalize : bool
        Shifts each video to the range `(0, 1)` by subtracting the minimum 
        and dividing by the difference between the maximum and the minimum 
        pixel value. Defaults to `False`
    data_format : str
        Video data format, either "channels_last" or "channels_first".

        * ``"channels_last"``: The tensor will have shape 
          ``(<videos>, <frames>, <height>, <width>, <channels>)``
        * ``"channels_first"``: The tensor will have shape 
          ``(<videos>, <channels>, <frames>, <height>, <width>)``

        ``channels`` will be **3** for videos in RGB format, or **1** 
        for videos in grayscale.
    random_state : int
        Integer that seeds the (numpy) random number generator, defaults 
        to 17. Used only when ``mode`` is set to "random".

    Example
    -------
    .. code-block:: python

       from mydia import Videos

       reader = Videos(
           target_size=(720, 480),
           to_gray=False,
           num_frames=128,
           data_format="channels_first"
       )

       video = reader.read("./path/to/video")

    Note
    ----
    You could also pass a `callable` to ``mode`` for custom frame 
    extraction. The `callable` should return a **list of integers**, 
    denoting the indices of the frames to be extracted. It should 
    take 4 (non-keyword) arguments: 

    * ``total_frames``: The total number of frames in the video
    * ``num_frames``: The number of frames that you want to extract
    * ``fps``: The frame rate of the video
    * ``random_state``: Integer to seed the random number generator

    These arguments may/may not be used to generate the required 
    frame indices. Detailed examples are provided in the documentation.

    Warning
    -------
    If you are passing a `callable` to ``mode``, then make sure that 
    the number of frames (indices) it returns is equal to the value of 
    ``num_frames``. If this condition is not met, then this would mean 
    that the number of frames selected is different for different videos, 
    and therefore they cannot be stacked into a single tensor.

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

        self.random_state = random_state

    def read(self, paths, verbose=1, workers=0):
        """Function to read videos

        Parameters
        ----------
        paths : str or list[str]
            A list of paths/path of the video(s) to be read.
        verbose : int
            If set to 0, the progress bar will be disabled.
        workers : int
            The number of processes (CPUs) to use for reading the videos. 
            This uses the ``multiprocessing`` module present in the python 
            standard library.

            Its value can range from 0 to `max_workers` where the latter 
            can be determined by calling ``multiprocessing.cpu_count()`` 
            on your machine.

            Defaults to 0, which means that multiprocessing will **not** 
            be used.

        Returns
        -------
        :obj:`numpy.ndarray`
            A 5-dimensional tensor, whose shape will depend on the value 
            of ``data_format``.
            
            * For ``"channels_last"``: The tensor will have shape 
              ``(<videos>, <frames>, <height>, <width>, <channels>)``
            * For ``"channels_first"``: The tensor will have shape 
              ``(<videos>, <channels>, <frames>, <height>, <width>)``

        Raises
        ------
        ValueError
            If ``paths`` is neither a string, not a list of strings.
        IndexError
            If ``num_frames`` is set to a value greater than the total 
            number of frames available in the video.

        Important
        ---------
        If multiple videos are to be read, then each video should have 
        the same dimension ``(frames, height, width)``, otherwise they 
        cannot be stacked into a single tensor. Therefore, the user **must** 
        use the parameters ``target_size`` and ``num_frames`` to make 
        sure of this.

        """
        if not isinstance(paths, list):
            if isinstance(paths, str):
                paths = [paths]
            else:
                raise ValueError("Invalid value of 'paths'")
        disable = False
        if verbose == 0:
            disable = True

        video_tensor = None
        if (isinstance(workers, int)) and (workers > 0):
            video_tensor = self._read_parallel(paths, disable, workers)
        else:
            paths_iterator = tqdm(paths, unit="videos", disable=disable)
            video_tensor = np.vstack(map(self._read_video, paths_iterator))

        if self.data_format == "channels_first":
            video_tensor = np.transpose(video_tensor, axes=(0, 4, 1, 2, 3))

        return video_tensor

    def _read_parallel(self, paths, disable, workers):
        """Used internally by :func:`read()` to read the videos in parallel.

        This uses the ``multiprocessing`` module present in the python 
        standard library.

        The function is constructed in a way so as to guarantee the 
        reproducibility of frames, irrespective of the `mode` used for 
        frame selection.

        """
        max_workers = cpu_count()
        if workers > max_workers:
            warnings.warn(f"The CPU can support maximum {max_workers} workers.")
            workers = max_workers
        list_of_videos = []
        with Pool(workers) as pool:
            with tqdm(total=len(paths), unit="videos", disable=disable) as pbar:
                for _, result in enumerate(pool.imap(self._read_video, paths)):
                    list_of_videos.append(result)
                    pbar.update()
        pool.join()

        return np.vstack(list_of_videos)

    def _read_video(self, path):
        """Used internally by :func:`read()` to read in a **single** video.

        Parameters
        ----------
        path : str
            The path of the video to be read.

        Returns
        -------
        :obj:`numpy.ndarray`
            A 5-dimensional tensor, whose shape will depend on the value 
            of ``data_format``

            * For ``"channels_last"``: The tensor will have shape 
              ``(1, <frames>, <height>, <width>, <channels>)``
            * For ``"channels_first"``: The tensor will have shape 
              ``(1, <channels>, <frames>, <height>, <width>)``

        """
        fps, total_frames = self._probe(path)
        width = self.target_size.width
        height = self.target_size.height

        out = ffmpeg.input(filename=path)

        if self.num_frames is not None:
            if self.num_frames <= total_frames:
                indices = self.mode(
                    total_frames, self.num_frames, fps, self.random_state
                )
                temp_msg = """The number of frames to be selected returned 
                by the callable does not match the value of the parameter 
                'num_frames'. Your callable should return the same number 
                of frames for every video, regardless of their individual 
                duration."""
                assert len(indices) == self.num_frames, temp_msg
                select_str = "+".join([f"eq(n,{idx})" for idx in indices])
                out = out.filter("select", select_str)
            else:
                raise IndexError(
                    "The value of 'num_frames' is greater than the total "
                    "number of frames available"
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

        Note
        ----
        This function also sets the `default` dimensions of the video, 
        if the frames are not to be resized.

        Parameters
        ----------
        path : str
            The path of the video to be read.

        Returns
        -------
        tuple[int, int]
            Frame rate and the total number of frames in the video.

        """
        try:
            probe = ffmpeg.probe(filename=path)
        except Exception as e:
            # The exception returned by `ffprobe` is in bytes
            print(e.stderr.decode())
        else:
            video_stream = next(
                (
                    stream
                    for stream in probe["streams"]
                    if stream["codec_type"] == "video"
                ),
                None,
            )

            # If the frame rate is 25, then the 'avg_frame_rate' is of
            # the form `25/1`
            fps = int(video_stream["avg_frame_rate"].split("/")[0])
            total_frames = int(video_stream["nb_frames"])
            if self.target_size is None:
                self.target_size = TargetSize(
                    width=video_stream["width"], height=video_stream["height"]
                )

            return (fps, total_frames)

        # The method will return nothing if an exception is encountered


def make_grid(video, num_col=3, padding=5):
    """Converts a video into a grid of frames.

    Parameters
    ----------
    video : :obj:`numpy.ndarray`
        A 4-dimensional video tensor (a single video).
    num_col : int
        The number of columns in the grid, defaults to 3.
    padding : int
        Amount of padding (in pixels), defaults to 5.

    Returns
    -------
    :obj:`numpy.ndarray`
        A gird of frames (numpy array) of shape ``(height, width, 3)`` 
        if the video is in RGB format, or ``(height, width)`` if the 
        video is in grayscale.

    Raises
    ------
    ValueError
        If the dimension of the ``video`` tensor is invalid.

    Example
    -------
    .. code-block:: python
       :emphasize-lines: 7, 8

       import matplotlib.pyplot as plt
       from mydia import Videos, make_grid

       reader = Videos(target_size=(720, 480), to_gray=True)
       video = reader.read("./path/to/video")

       grid = make_grid(video[0], num_col=6, padding=8)
       plt.imshow(grid, cmap="gray")

    """
    if video.ndim != 4:
        raise ValueError("Invalid value for 'video'")

    # If the channels are not at the end, then the format of the video
    # is `channels_first` which needs to be converted to `channels_last`
    if not ((video.shape[-1] == 1) or (video.shape[-1] == 3)):
        video = np.transpose(video, axes=(1, 2, 3, 0))

    num_frames = video.shape[0]
    new_height = video.shape[1] + padding
    new_width = video.shape[2] + padding
    channels = video.shape[3]

    num_row = int(np.ceil(num_frames / num_col))
    frame_pad = ((0, 0), (0, padding), (0, padding), (0, 0))
    grid_pad = ((padding, 0), (padding, 0), (0, 0))
    extra_frames = (num_row * num_col) - num_frames

    video = np.pad(video, pad_width=frame_pad, mode="constant", constant_values=0)
    video.resize(
        (num_frames + extra_frames, new_height, new_width, channels)
    )  # Appends the extra (empty) frames to the video tensor
    video = (
        video.reshape(num_row, num_col, new_height, new_width, channels)
        .transpose((0, 2, 1, 3, 4))
        .reshape(num_row * new_height, num_col * new_width, channels)
    )
    video = np.pad(video, pad_width=grid_pad, mode="constant", constant_values=0)

    if channels == 1:
        video = video[:, :, 0]

    return video
