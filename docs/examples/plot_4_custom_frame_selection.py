"""
Custom frame selection
======================

By default, you can use one of the five available options for frame selection - 
`{"auto"`, `"random"`, `"first"`, `"last"`, and `"middle"}`, by passing it to the 
parameter ``mode``. (View the documentation of :class:`mydia.Videos` for more 
information on what each of these does)

Internally, each of these options are mapped to a `callable` that returns a list 
of integers denoting the indices of the frames to be selected. The `callable` 
takes 3 non-keyword arguments:

* ``total_frames`` (`int`): The total number of frames in the video
* ``num_frames`` (`int`): The number of frames that you want to extract
* ``fps`` (`int`): The frame rate of the video

You could create your own `callable` and pass it to the parameter ``mode``, gaining 
immense flexibility in the frame selection process.

The general format of the `callable` should be:

.. code:: python

   def func(total_frames, num_frames, fps):
       # Create a list of integers denoting the required frame indices
       frames_indices = []
       # Do something
       ...

       return frame_indices

.. note::

   1. There are no tests that validate the indices returned by the `callable` and 
      therefore, they must be within the range of ``total_frames``.

   2. Also, the frames are **not** repeated. That is, even if there are repeated 
      indices, the number of frames are selected only for the unique values in the 
      index array.

Examples
~~~~~~~~

* Let's say we want the first 20 even numbered frames (starting from 0, 2, 4, ...), 
  assuming that the video has more that 20x2 = 40 frames.
  
"""

# Imports
import matplotlib.pyplot as plt
from mydia import Videos, plot

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Custom frame selector
# `*args` is used because we do not need the arguments for generating the 
# index array
def even_frames(*args):
    return [i for i in range(0, 40, 2)]

# Configuring the parameters
# Passing `even_frames` to `mode`
reader = Videos(
    target_size=(720, 480),
    to_gray=True,
    num_frames=20,
    mode=even_frames,
)

# Call the 'read()' function to get the required video tensor
# which will be of shape (1, 20, 480, 720, 3)
video = reader.read(video_path)
print("The shape of the tensor:", video.shape)

# Plot the video frames in a grid
plot(video[0])
plt.show()

################################################################################
# * Now, let's try something a little more complicated. We will select the first 
#   3 frames for each second of the video
# 
#   For example, suppose we have a video with a total of 70 frames with a frame 
#   rate of 25. This means that the duration of the video is ~3 seconds (25 frames, 
#   25 frames, 20 frames). Now, we need the first 3 frames for each second of the 
#   video. 
# 
# **Given below is a method to select first `N` frames from each second of a video:**

# Imports
import matplotlib.pyplot as plt
import numpy as np
from mydia import Videos, plot

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Custom frame selector
N = 3
def frames_per_second(total_frames, num_frames, fps):
    t = np.arange(total_frames)
    f = np.arange(fps)
    mask = np.resize(f, total_frames)

    return t[mask < N]

# Configuring the parameters
reader = Videos(
    target_size=(720, 480),
    num_frames=18,
    mode=frames_per_second,
)

# Call the 'read()' function to get the required video tensor
# which will be of shape (1, 18, 480, 720, 1)
video = reader.read(video_path)
print("The shape of the tensor:", video.shape)

# Plot the video frames in a grid
plot(video[0], num_col=3)
plt.show()
