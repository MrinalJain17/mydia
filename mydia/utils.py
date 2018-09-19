from typing import List, NamedTuple

import numpy as np


class TargetSize(NamedTuple):
    """A named tuple representing tha target size of frames of a video"""
    width: int
    height: int
    rescale: bool = False


def _mode_auto(total_frames: int, num_frames: int, fps: int) -> List[int]:
    """The :code:`auto` mode for frame extraction

    Refer to the documentation of the class :code:`Videos` for further details.
    
    """
    return np.linspace(
        0, total_frames, num_frames, endpoint=False, dtype=np.int
    ).tolist()


def _mode_random(total_frames: int, num_frames: int, fps: int) -> List[int]:
    """The :code:`random` mode for frame extraction

    Refer to the documentation of the class :code:`Videos` for further details.
    
    """
    return np.sort(
        np.random.choice(total_frames, size=num_frames, replace=False)
    ).tolist()


def _mode_first(total_frames: int, num_frames: int, fps: int) -> List[int]:
    """The :code:`first` mode for frame extraction

    Refer to the documentation of the class :code:`Videos` for further details.
    
    """
    indices = np.arange(total_frames)
    return indices[:num_frames].tolist()


def _mode_last(total_frames: int, num_frames: int, fps: int) -> List[int]:
    """The :code:`last` mode for frame extraction

    Refer to the documentation of the class :code:`Videos` for further details.
    
    """
    indices = np.arange(total_frames)
    return indices[(total_frames - num_frames) :].tolist()


def _mode_middle(total_frames: int, num_frames: int, fps: int) -> List[int]:
    """The :code:middle` mode for frame extraction

    Refer to the documentation of the class :code:`Videos` for further details.
    
    """
    indices = np.arange(total_frames)
    # No. of frames to remove from the front
    front = ((total_frames - num_frames) // 2) + 1
    return indices[front : (front + num_frames)].tolist()
