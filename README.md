# Video Utilities

__*Read videos as numpy arrays, with a gamut of additional functionalities.*__

### Installation

* **Install Mydia from PyPI (recommended):**

```bash
pip install Mydia
```

* **Alternatively, install from Github source:**

First, clone the repository.

```bash
git clone https://github.com/MrinalJain17/Mydia.git
```

Then, build the module

```bash
cd Mydia
python setup.py install
```

### Getting started

##### *Let's read in a video*

```python
from mydia import Videos

video_path = r'./static/sample_video/bigbuckbunny.mp4'
reader = Videos()

video = reader.read(video_path)   # a tensor of shape (1, 132, 720, 1080, 3)
```

The tensor represents **1 video** having **132 frames**, with each frame having a width and height of 1080 and 720 pixels respectively. `3` denotes the *RGB channels* of the video.

##### *Extracting only 9 frames (at equal intervals) from the entire video and resizing each frame to be 720 pixels in width and 480 pixels in height.*

```python
from mydia import Videos

video_path = r'./static/sample_video/bigbuckbunny.mp4'
reader = Videos(target_size=(720, 480), 
                num_frames=9)

video = reader.read(video_path)   # a tensor of shape (1, 9, 480, 720, 3)

reader.plot(video[0])   # Plotting the frames of the video in a grid
```

![Video frames](https://github.com/MrinalJain17/Mydia/raw/master/static/images/video_frames.PNG)

*Hmm.. Let's read the same video in __gray scale__.*

```python
from mydia import Videos

video_path = r'./static/sample_video/bigbuckbunny.mp4'
reader = Videos(target_size=(720, 480), 
                to_gray=True, 
                num_frames=9)

video = reader.read(video_path)   # a tensor of shape (1, 9, 480, 720, 1)

reader.plot(video[0])   # Plotting the frames of the video in a grid
```

![Video frames](https://github.com/MrinalJain17/Mydia/raw/master/static/images/video_frames_gray.PNG)

## Requirements
`Python 3.x` (preferably from the [Anaconda Distribution](https://www.anaconda.com/download/))

The program uses [Scikit-video](http://www.scikit-video.org/stable/), which requires `FFmpeg` to be installed on the system.  
To install `FFmpeg` on your machine

For **Linux**:

		$ sudo apt-get update
		$ sudo apt-get install libav-tools

For **Windows or MAC/OSX**:  
Download the required binaries from [here](https://www.ffmpeg.org/download.html). Extract the zip file and add the location of binaries to the `PATH` variable

### Additional Libraries to install:

Several libraries like [Numpy](http://www.numpy.org/), [Pillow](https://python-imaging.github.io/), [Matplotlib](https://matplotlib.org/) etc., required for the package come pre-installed with the Anaconda distribution of Python.  
Install the following extra packages (if not already installed):

- [Scikit-video](http://www.scikit-video.org/stable/)

	```
		pip install sk-video
	```

- [tqdm](https://pypi.python.org/pypi/tqdm#installation) - Required for displaying the progress bar.

	```
		pip install tqdm
	```
