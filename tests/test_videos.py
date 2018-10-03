import numpy as np
import pytest
from mydia import Videos

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
    def custom(total_frames, num_frames, fps):
        return [i for i in range(0, total_frames, 2)]

    reader = Videos(target_size=(360, 240), to_gray=True, num_frames=36, mode=custom)
    reader.read(path, verbose=0)
