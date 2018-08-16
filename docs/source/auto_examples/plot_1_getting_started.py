"""
Get started with some basics
============================

Reading videos into NumPy arrays was never more simple. In addition,
this library also provides an entire range of additional functionalities
for reading the videos.
"""

##############################################################################
# How to simply read a video, given its path?
# -------------------------------------------

# Import
from mydia import Videos

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Create a reader object
reader = Videos()

# Call the 'read()' function to get the video tensor
video = reader.read(video_path)

# a tensor of shape (1, 132, 720, 1080, 3)
print("The shape of the tensor:", video.shape)

##############################################################################
# The tensor represents **1 video** having **132 frames**, with each frame
# having a width and height of 1080 and 720 pixels respectively. “**3**”
# denotes the Red, Green and Blue (RGB) channels of the video.
#
#
# Or, read multiple videos
# ------------------------
#
# .. code:: python
#
#  from mydia import Videos
#  video_paths = ["", "", ...] # list of path of videos
#  reader = Videos()
#  video = reader.read(video_paths)
#
# *For detailed information of the output tensor, view the code documentation.*
#
#
# Saving the loaded video tensor
# ------------------------------
#
# .. important:: Once the videos have been processed, they could be saved
#  as :obj:`numpy.ndarray` (in .npz or .npy format). For further details, view
#  the documentation of:
#
#  - :obj:`numpy.save`: for saving in .npy format
#
#  - :obj:`numpy.savez`: for saving in .npz format
#
#  - :obj:`numpy.load`: for loading back the saved numpy tensors
#
#  Since the whole reading process is time consuming, this could turn out to be
#  a useful way to store and reload the video tensors.
