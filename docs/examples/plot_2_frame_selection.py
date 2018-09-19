"""
Frame selection and resizing
============================

-  We want to resize each frame to be 720 pixels in width and 480 pixels
   in height.
-  Not all the frames are required. Let’s just capture exactly 12 frames
   (at equal intervals) from the video.
-  And finally, we’ll also visualize the captured frames.
"""

# Imports
import matplotlib.pyplot as plt
from mydia import Videos, plot

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Configuring the parameters
# Setting 'target_size' = (720, 480) : this denotes the new width and height of the frames
# Setting 'num_frames' = 12 : to capture exactly 12 frames
# For more detailed information, view the code documentation.
reader = Videos(target_size=(720, 480), num_frames=12)

# Call the 'read()' function to get the required video tensor
video = reader.read(video_path)  # a tensor of shape (1, 12, 480, 720, 3)

# Plot the video frames in a grid
plot(video[0])
plt.show()

##############################################################################
# .. note:: The number of channels for a RGB video is 3
#  (indicated by the last value in the tuple).
