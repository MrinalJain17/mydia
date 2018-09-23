"""
Generating videos for memeory efficiency
========================================

There is no formal generator provided by the module, however you could follow 
the given steps to create a generator if you are dealing with a large number of 
videos (that couldn't be stored in the memory at once).

**Assuming that a list of video paths is available, we will create a generator 
of these videos.**

"""

# Imports
from mydia import Videos

# Initialize video path
video_path = r"./sample_video/bigbuckbunny.mp4"

# Let's use the same video in this examples multiple times (for simplicity)
videos_path = [video_path for i in range(3)]

# Configuring the parameters
# For other paramaters available, view the code documentation.
reader = Videos(
    target_size=(720, 480),
    num_frames=30,
    mode="auto",
)

# This generator will generate videos from the list of paths
def generate_video():
    for path in videos_path:
        video = reader.read(path)
        yield video

# Using the videos one-by-one
for i in range(len(videos_path)):
    vid = next(generate_video())
    print(f"The shape of the tensor of video {i+1}:", vid.shape)
