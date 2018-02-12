# Video Utilities
Contains functions to read videos as NumPy arrays in Python

Read the documentation at [mrinaljain17.github.io/video_utils](https://mrinaljain17.github.io/video_utils/)

## Instructions
1. Clone the repository and navigate to the downloaded folder.

	```
		git clone https://github.com/MrinalJain17/video_utils.git
		cd video_utils
	```
2. In order to read the videos, there is a helper class `Videos` in `utils.py`.

	```python
		import numpy as np
		from utils import Videos
		
		reader = Videos(target_size=(150, 25), 
				to_gray=True, 
				max_frames=60, 
				extract_frames='first', 
				required_fps=0, 
				normalize_pixels=(0, 1))
		
		paths = [..]    # List of strings - each string being the path (absolute) of a video
		videos = reader.read_videos(paths)
	```
3. View this [jupyter notebook]() to see how to get started

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
Install the following extra packages:

- [Scikit-video](http://www.scikit-video.org/stable/)

	```
		pip install sk-video
	```

- [tqdm](https://pypi.python.org/pypi/tqdm#installation) - Required for displaying the progress bar.

	```
		pip install tqdm
	```
