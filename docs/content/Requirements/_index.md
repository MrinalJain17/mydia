---
title: "Requirements"
date: 2018-04-13T18:58:18+05:30
weight: 2
---

`Python 3.x` (preferably from the [Anaconda Distribution](https://www.anaconda.com/download/))

The program uses [Scikit-video](http://www.scikit-video.org/stable/), which requires `FFmpeg` to be installed on the system.  
To install `FFmpeg` on your machine

For **Linux** users:

```bash
$ sudo apt-get update
$ sudo apt-get install libav-tools
```

For **Windows or MAC/OSX** users:  
Download the required binaries from [here](https://www.ffmpeg.org/download.html). Extract the zip file and add the location of binaries to the `PATH` variable

### Additional Libraries to install:

Several libraries like [Numpy](http://www.numpy.org/), [Pillow](https://python-imaging.github.io/), [Matplotlib](https://matplotlib.org/) etc., required for the package come pre-installed with the Anaconda distribution for Python.  
Install the following extra packages (if not already installed):

- [Scikit-video](http://www.scikit-video.org/stable/)

```bash
	pip install sk-video
```

- [tqdm](https://pypi.python.org/pypi/tqdm#installation) - Required for displaying the progress bar.

```bash
	pip install tqdm
```