"""Contains the callables for the built-in frame selection modes.

Refer to the documentation of the class :class:`Videos` for further
details on their usage.

"""

from typing import List

import numpy as np


def _mode_auto(total_frames: int, num_frames: int, fps: int, *args) -> List[int]:
    """The ``auto`` mode for frame extraction"""
    return np.linspace(
        0, total_frames, num_frames, endpoint=False, dtype=np.int
    ).tolist()


def _mode_random(
    total_frames: int, num_frames: int, fps: int, random_state: int
) -> List[int]:
    """The ``random`` mode for frame extraction"""
    r = np.random.RandomState(random_state)
    return np.sort(r.choice(total_frames, size=num_frames, replace=False)).tolist()


def _mode_first(total_frames: int, num_frames: int, fps: int, *args) -> List[int]:
    """The ``first`` mode for frame extraction"""
    indices = np.arange(total_frames)
    return indices[:num_frames].tolist()


def _mode_last(total_frames: int, num_frames: int, fps: int, *args) -> List[int]:
    """The ``last`` mode for frame extraction"""
    indices = np.arange(total_frames)
    return indices[(total_frames - num_frames) :].tolist()


def _mode_middle(total_frames: int, num_frames: int, fps: int, *args) -> List[int]:
    """The ``middle`` mode for frame extraction"""
    indices = np.arange(total_frames)
    # No. of frames to remove from the front
    front = ((total_frames - num_frames) // 2) + 1
    return indices[front : (front + num_frames)].tolist()
