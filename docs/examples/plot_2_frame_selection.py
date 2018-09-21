"""
Frame selection, resizing, and grayscale conversion
===================================================

* We want to resize each frame to be 720 pixels in width and 480 pixels
  in height.

  * Set ``target_size`` to (720, 480)

* All the frames are not required. Let’s just capture exactly 12  random
  frames from the video.

  * Set ``mode`` to ``"random"``

* And finally, visualize the captured frames using ``mydia.plot``
"""

# Imports
import matplotlib.pyplot as plt
from mydia import Videos, plot

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Configuring the parameters
# For other paramaters available, view the code documentation.
reader = Videos(
    target_size=(720, 480), 
    num_frames=12, 
    mode="random",
)

# Call the 'read()' function to get the required video tensor
# which will be of shape (1, 12, 480, 720, 3)
video = reader.read(video_path) 

# Plot the video frames in a grid
plot(video[0])
plt.show()

##############################################################################
# .. note:: The number of channels for a RGB video is 3
#  (indicated by the last value in the tuple).
# 
# 
# * Now let's read the video with the same configuration, but in **grayscale**
#   
#   * For this, set ``to_gray`` to `True`

# Imports
import matplotlib.pyplot as plt
from mydia import Videos, plot

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Configuring the parameters
reader = Videos(
    target_size=(720, 480), 
    to_gray=True, 
    num_frames=12, 
    mode="random",
)

# Call the 'read()' function to get the required video tensor
# which will be of shape (1, 12, 480, 720, 1)
video = reader.read(video_path)

# Plot the video frames in a grid
plot(video[0])
plt.show()

##############################################################################
# .. note:: The number of channels for a video in gray scale is 1
#  (indicated by the last value in the tuple).
