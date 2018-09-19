"""Mydia: Read videos as numpy arrays

The class `Videos` in this module can be used to read videos with advance support
for frame selection, frame resizing and normalization.

The module is a wrapper around the library `ffmpeg-python`, and uses `FFmpeg` as 
its backend to process the videos.

"""

__version__ = "2.0.0b"
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
    """

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
        """
        
        """

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
        """
        
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
        """
        
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

    def read(self, paths: Union[str, List[str]]):
        """
        
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
