import numpy as np
import pytest
from mydia import Videos, make_grid

path = "./docs/examples/sample_video/bigbuckbunny.mp4"
settings = [
    (None, False, None, False, (1, 132, 720, 1280, 3)),
    ((360, 240), True, 36, False, (1, 36, 240, 360, 1)),
    ((360, 240), True, 36, True, (1, 36, 240, 360, 1)),
]


@pytest.mark.parametrize(
    ("target_size", "to_gray", "num_frames", "normalize", "expected_shape"), settings
)
def test_reader(target_size, to_gray, num_frames, normalize, expected_shape):
    reader = Videos(
        target_size=target_size,
        to_gray=to_gray,
        num_frames=num_frames,
        normalize=normalize,
    )
    video = reader.read(path, verbose=0)
    if not normalize:
        assert video.shape == expected_shape
    else:
        assert (np.min(video) >= 0) and (np.max(video) <= 1)


@pytest.mark.xfail(
    raises=AssertionError,
    reason="The number of frames to select returned by the custom function is "
    "not equal to `num_frames`.",
)
def test_custom_frame():
    def custom(total_frames, num_frames, fps, *args):
        return [i for i in range(0, total_frames, 2)]

    reader = Videos(target_size=(360, 240), to_gray=True, num_frames=36, mode=custom)
    reader.read(path, verbose=0)


def test_random_repeatability():
    reader_1 = Videos(target_size=(360, 240), to_gray=True, num_frames=36, mode="random", random_state=26)
    reader_2 = Videos(target_size=(360, 240), to_gray=True, num_frames=36, mode="random", random_state=26)

    video_1 = reader_1.read(path, verbose=0)
    video_2 = reader_2.read(path, verbose=0)

    assert np.array_equal(video_1, video_2) == True

def test_make_grid():
    target_width = 360
    target_height = 240
    padding = 5
    num_frames = 36
    num_col = 5

    reader = Videos(target_size=(target_width, target_height), to_gray=False, num_frames=num_frames)
    video = reader.read(path, verbose=0)
    num_row = int(np.ceil(num_frames / num_col))
    grid = make_grid(video[0], num_col=num_col, padding=padding)
    grid_width = (target_width * num_col) + (padding * (num_col + 1))
    grid_height = (target_height * num_row) + (padding * (num_row + 1))

    assert grid.shape == (grid_height, grid_width, 3)
