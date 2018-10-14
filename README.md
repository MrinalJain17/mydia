# Mydia
[![Build Status](https://travis-ci.com/MrinalJain17/mydia.svg?branch=master)](https://travis-ci.com/MrinalJain17/mydia)

Reading videos into NumPy arrays was never more simple. This library provides 
an entire range of additional functionalities such as custom frame selection, 
frame resizing, pixel normalization, grayscale conversion and much more.

[READ THE DOCUMENTATION](https://mrinaljain17.github.io/mydia)

## Getting started

**How to simply read a video, given its path?**

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
- `3` denotes that the video is RGB

### View detailed examples [here](https://mrinaljain17.github.io/mydia/auto_examples/)

## Installation

- **Install using Conda Package Manager (Recommended):**

    ```bash
        conda install -c mrinaljain17 mydia
    ```

- **Install from PyPI:**

    ```bash
        pip install mydia
    ```

- **Alternatively, install from source:**

  First, clone the repository

    ```bash
        git clone https://github.com/MrinalJain17/mydia.git
    ```

  Then, build the module

    ```bash
        cd mydia
        python setup.py install
    ```

## Requirements

`Python 3.x` (preferably from the [Anaconda Distribution](https://www.anaconda.com/download/))

The program uses [ffmpeg-python](https://github.com/kkroening/ffmpeg-python), which provides
python bindings for [FFmpeg](https://www.ffmpeg.org/) (used as the backend for reading and 
processing videos)

To install `FFmpeg` on your machine:

For **Linux** users - 

```bash
    $ sudo apt-get update
    $ sudo apt-get install libav-tools
```

**OR**

```bash
    $ sudo apt-get update
    $ sudo apt-get install ffmpeg
```

For **Windows or MAC/OSX** users - 

Download the required binaries from [here](https://www.ffmpeg.org/download.html). 
Extract the zip file and add the location of binaries to the `PATH` variable.

### Required Libraries

Install the following packages along with their dependencies:

- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)
- [Numpy](http://www.numpy.org/)
- [tqdm](https://pypi.python.org/pypi/tqdm#installation) - Required for displaying the 
  progress bar.

```bash
    pip install ffmpeg-python numpy tqdm
```
