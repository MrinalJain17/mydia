# Mydia
[![Build Status](https://travis-ci.org/MrinalJain17/mydia.svg?branch=master)](https://travis-ci.org/MrinalJain17/mydia)
![Code Style](https://img.shields.io/badge/code%20style-black-black.svg)
![Platform](https://img.shields.io/badge/Platforms-linux--64,osx--64,win--64-orange.svg)

Reading videos as NumPy arrays was never more simple. This library provides an 
entire range of additional functionalities such as custom frame selection, frame 
resizing, pixel normalization, grayscale conversion and much more.

[**READ THE DOCUMENTATION**](https://mrinaljain17.github.io/mydia)

## Getting started

#### 1. Read a video, given its path

```python

# Import
from mydia import Videos

# Initialize video path
video_path = r".docs/examples/sample_video/bigbuckbunny.mp4"

# Create a reader object
reader = Videos()

# Call the 'read()' function to get the video tensor
# which will be of shape (1, 132, 720, 1280, 3)
video = reader.read(video_path)

```

The tensor can be interpreted as:

- 1 video
- Having 132 frames, 
- Dimension (width x height) of each frame: 1280x720 pixels
- `3` denotes that the video is in RGB format

#### 2. You can even use multiple workers for reading the videos in parallel

```python

from mydia import Videos

video_paths = [
    "path/to/video_1", 
    "path/to/video_2", 
    "path/to/video_3",
    ...,
]

reader = Videos()
video = reader.read(video_path, workers=4)

```

#### 3. View detailed examples [here](https://mrinaljain17.github.io/mydia/auto_examples/)

## Requirements

- `Python 3.x` (preferably from the [Anaconda Distribution](https://www.anaconda.com/download/))

- [`FFmpeg`](https://www.ffmpeg.org/): The backend for reading and processing 
  the videos.

  **The recommended (and probably the easiest) way of installing `FFmpeg` is 
  via the conda package manager.**

  ```bash
      conda install -c mrinaljain17 ffmpeg
  ```

  However, if you are not using *conda*, then
  
  For **Linux** users - 
  
  ```bash
      $ sudo apt-get update
      $ sudo apt-get install ffmpeg
  ```
  
  For **Windows or MAC/OSX** users - 
  
  Download the required binaries from [here](https://www.ffmpeg.org/download.html). 
  Extract the zip file and add the location of binaries to the `PATH` variable.

## Installation

1. **Using the conda package manager (recommended):**

    ```bash
        conda install -c mrinaljain17 mydia
    ```

2. **Using pip:**

    ```bash
        pip install mydia
    ```

The following python packages that `mydia` depends on, will also be 
installed, along with their dependencies.

- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [Numpy](http://www.numpy.org/)
- [tqdm](https://pypi.python.org/pypi/tqdm#installation) - Required for 
  displaying the progress bar.

## License

Copyright 2018 [Mrinal Jain](https://mrinaljain17.github.io/).

Released under the [MIT License](https://mrinaljain17.github.io/license/).
