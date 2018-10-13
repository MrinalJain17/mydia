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
* ``random_state`` (:obj:`numpy.random.RandomState`): A RandomState object to seed the 
  random number generator

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

.. warning::

   If you are passing a `callable` to ``mode``, then make sure that the number of frames 
   (indices) it returns is equal to the value set in ``num_frames``. If this condition is 
   not met, then this would mean that the number of frames selected is different for 
   different videos, and therefore they cannot be stacked into a single tensor.

Examples
~~~~~~~~

* Let's say we want the first 20 even numbered frames (starting from 0, 2, 4, ...), 
  assuming that the video atleast 20x2 = 40 frames.
  
"""

# Imports
import matplotlib.pyplot as plt
from mydia import Videos, make_grid

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
grid = make_grid(video[0], num_col=4)
plt.imshow(grid, cmap="gray")

##############################################################################
# *Note that `make_grid` can also take some arguments for customizing the grid. For more 
# info, view the documentation of the function* :func:`mydia.make_grid`.
