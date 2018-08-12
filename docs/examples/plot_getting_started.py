"""
Get started with some basics
============================

Reading videos into NumPy arrays was never more simple. In addition,
this library also provides an entire range of additional functionalities
for reading the videos.
"""

##############################################################################
# How to simple read a video, given its path?
# -------------------------------------------

# Import
from mydia import Videos
import matplotlib.pyplot as plt

# Initialize video path
video_path = r'./sample_video/bigbuckbunny.mp4'

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

##############################################################################
# Now, let’s try to be a little more specific
# -------------------------------------------

##############################################################################
#-  We want to resize each frame to be 720 pixels in width and 480 pixels
#   in height.
#-  Not all the frames are required. Let’s just capture exactly 12 frames
#   (at equal intervals) from the video.
#-  And finally, we’ll also visualize the captured frames.

# Import
from mydia import Videos
import matplotlib.pyplot as plt

# Initialize video path
video_path = r'./sample_video/bigbuckbunny.mp4'

# Configuring the parameters
# Setting 'target_size' = (720, 480) : this denotes the new width and height of the frames
# Setting 'num_frames' = 12 : to capture exactly 12 frames
# For more detailed information, view the code documentation.
reader = Videos(target_size=(720, 480), 
                num_frames=12)

# Call the 'read()' function to get the required video tensor
video = reader.read(video_path)   # a tensor of shape (1, 12, 480, 720, 3)

# Plot the video frames in a grid
reader.plot(video[0])
plt.show()

##############################################################################
# Great! Now let’s read the same video in **gray scale**, instead of RGB.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##############################################################################
#.. note:: The number of channels for a video in gray scale is 1 
# (indicated by the last value in the tuple).

# Import
from mydia import Videos
import matplotlib.pyplot as plt

# Initialize video path
video_path = r'./sample_video/bigbuckbunny.mp4'

# Configuring the parameters
# Other parameters are the same as described above.
# The only additional parameter to modify is 'to_gray'
reader = Videos(target_size=(720, 480), 
                to_gray=True, 
                num_frames=12)

# Call the 'read()' function to get the required video tensor
video = reader.read(video_path)   # a tensor of shape (1, 12, 480, 720, 1)

# Plot the video frames in a grid
reader.plot(video[0])
plt.show()

##############################################################################
# Saving the loaded video tensor
# ------------------------------

##############################################################################
#.. important:: Once the videos have been processed, they could be saved 
# as :obj:`numpy.ndarray` (in .npz or .npy format). For further details, view 
# the documentation of: 
# 
# - :obj:`numpy.save`: for saving in .npy format 
# 
# - :obj:`numpy.savez`: for saving in .npz format 
# 
# - :obj:`numpy.load`: for loading back the saved numpy tensors 
# 
# Since the whole reading process is time consuming, this could turn out to be 
# a useful way to store and reload the video tensors. 
