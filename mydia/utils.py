from typing import List, NamedTuple

import numpy as np


class TargetSize(NamedTuple):
    width: int
    height: int
    rescale: bool = False


def _mode_auto(total_frames: int, num_frames: int, fps: int) -> List[int]:
    return np.linspace(
        0, total_frames, num_frames, endpoint=False, dtype=np.int
    ).tolist()


def _mode_random(total_frames: int, num_frames: int, fps: int) -> List[int]:
    return np.sort(
        np.random.choice(total_frames, size=num_frames, replace=False)
    ).tolist()


def _mode_first(total_frames: int, num_frames: int, fps: int) -> List[int]:
    indices = np.arange(total_frames)
    return indices[:num_frames].tolist()


def _mode_last(total_frames: int, num_frames: int, fps: int) -> List[int]:
    indices = np.arange(total_frames)
    return indices[(total_frames - num_frames) :].tolist()


def _mode_middle(total_frames: int, num_frames: int, fps: int) -> List[int]:
    indices = np.arange(total_frames)
    # No. of frames to remove from the front
    front = ((total_frames - num_frames) // 2) + 1
    return indices[front : (front + num_frames)].tolist()
