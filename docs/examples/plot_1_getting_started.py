"""
Get started with some basics
============================

"""

##############################################################################
# Simply read a video, given its path
# -----------------------------------

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
# The tensor can be interpreted as -
# 
# * 1 video
# * Having 132 frames, 
# * Dimension (width x height) of each frame: 1080x720 pixels
# * ``3`` denotes that the video is RGB
#
# Similarly, read multiple videos
# -------------------------------
#
# .. code:: python
#
#    from mydia import Videos
#
#    video_paths = [
#        "path/to/video_1", 
#        "path/to/video_2", 
#        "path/to/video_3",
#        ...,
#    ]          # list of path of videos
#
#    reader = Videos()
#    video = reader.read(video_paths)
#
# Or, use a python generator for multiple videos
# ----------------------------------------------
#
# .. code:: python
#
#    from mydia import Videos
#
#    video_paths = [
#        "path/to/video_1", 
#        "path/to/video_2", 
#        "path/to/video_3",
#        ...,
#    ]          # list of path of videos
#
#    reader = Videos()
#
#    def generate_video():
#        for path in video_paths:
#            video = reader.read(path)
#            yield video
#
#    for i in range(len(video_paths)):
#        vid = next(generate_video())
#        # Do something
#
# *For information on the parameters available, read the examples ahead and 
# also refer to the documentation of the class* :class:`mydia.Videos`.
#
#
# Saving the loaded video tensor
# ------------------------------
#
# .. important:: Once the videos have been processed, they could be saved
#  as :obj:`numpy.ndarray` (in `.npz` or `.npy` format). For further details, view
#  the documentation of:
#
#  * :obj:`numpy.save`: for saving in `.npy` format
#
#  * :obj:`numpy.savez`: for saving in `.npz` format
#
#  * :obj:`numpy.load`: for loading back the saved numpy tensors
#
#  Since the whole reading process is time consuming, this could turn out to be
#  a useful way to store and reload the video tensors.
