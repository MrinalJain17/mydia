---
title: "Mydia"
date: 2018-04-13T18:17:48+05:30
---

# Video Utilities

#### *Read videos as numpy arrays, with a gamut of additional functionalities.*

### Getting started

##### *Let's read in a video*

```python
from mydia import Videos

video_path = r'./static/sample_video/bigbuckbunny.mp4'
reader = Videos()

video = reader.read(video_path)   # a tensor of shape (1, 132, 720, 1080, 3)
```

The tensor represents **1 video** having **132 frames**, with each frame having a width and height of 1080 and 720 pixels respectively.  
`3` denotes the *RGB channels* of the video.

##### *Extracting only 9 frames (at equal intervals) from the entire video and resizing each frame to be 720 pixels in width and 480 pixels in height.*

```python
from mydia import Videos

video_path = r'./static/sample_video/bigbuckbunny.mp4'
reader = Videos(target_size=(720, 480), 
                num_frames=9)

video = reader.read(video_path)   # a tensor of shape (1, 9, 480, 720, 3)

reader.plot(video[0])   # Plotting the frames of the video in a grid
```

![Video frames](https://github.com/MrinalJain17/mydia/raw/master/static/images/video_frames.PNG)

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

![Video frames](https://github.com/MrinalJain17/mydia/raw/master/static/images/video_frames_gray.PNG)