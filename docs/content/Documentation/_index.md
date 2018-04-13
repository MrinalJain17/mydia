---
title: "Documentation"
date: 2018-04-13T19:00:51+05:30
weight: 3
---

### `class` mydia.Videos

To read in videos and store them as NumPy arrays.

The videos are stored as a 5-dimensional tensor - `(<No. of Videos>, <No. of frames>, <height>, <width>, <channels>)`.
The value of `channels` could be 1 (gray scale) or 3 (RGB).

### Parameters

+ **target_size** : *tuple*, optional  
    Tuple of form `(New_Width, New_Height)`, defaults to `None`.  
    A tuple denoting the target width and height (of the frames) of the videos. 
    If not set, the dimensions of the frames will not be altered.  
    
    **Note**  
    A single video is a stack of frames. If the dimension of all the frames is not the same, they cannot by stacked.

+ **to_gray** : *bool*, optional  
    If `True`, all the frames of the videos are converted to gray scale, defaults to `False`.

+ **mode** : *str*, optional  
    One of {"auto", "manual", "random"}, defaults to `auto`.  
    
    `auto`: The reader will read frames at equal intervals from the entire video. 
    The number of frames to be extracted (read) will depend on the value of `num_frames`.  
    `manual`: The user would manually provide the details to extract frames from the video. 
    Available parameters to tune are `num_frames`, `extract_position` and `required_fps`.  
    `random`: The reader will read frames at random from the entire video. 
    The number of frames to be extracted (read) will depend on the value of `num_frames`.

+ **num_frames** : *int*, optional  
    The (exact) number of frames to extract from each video, defaults to `None`.  
    Frames are extracted based on the value of `mode`.  
    If set to `None`, all the frames of the video would be kept.

    **Note**  
    Videos are stacked together. If the number of frames in all the videos are not the same, they cannot be stacked.

+ **extract_position** : *str*, optional  
    One of {"first", "middle", "last"}, defaults to `first`.  
    
    `first`: Extract the frames from the beginning of the video.  
    `last`: Extract the frames from the end of the video.  
    `middle`: Extract the frames from the middle of the video  
    (Removes `(total frames - 'max_frames') // 2` from the beginning as well as the end of the video)

+ **required_fps** : *int*, optional  
    The number of frame(s) to capture per second from the video, defaults to `None`.  
    
    *Example* :  
    Let the duration of a video to be 10 seconds and assume that it was captured at the rate of 30fps.  
    Suppose the value of `required_fps` is set to 7.  
    Then for each second, the **first** 7 frames would be captured.  
    The resulting video (in form of tensor) will have a total of 10 x 7 = 70 frames.

+ **normalize** : *bool*, optional  
    If `True`, then the pixel values will be normalized to be in range (0, 1), defaults to `False`.  

+ **random_state** : *int*, optional  
    The number to seed the random number generator (when using the `mode` as "random"), defaults to 17.

#### `read(paths)`
Function to read videos.

#### Parameters
+ **paths** : *list*  
    A list of paths of the videos to be read.

#### Returns
+ **numpy.ndarray**  
    A 5-dimensional tensor with shape `(<No. of videos>, <No. of frames>, <height>, <width>, <channels>)`.  
    The value of `channels` could be 1 (gray scale) or 3 (RGB).

#### `plot(video=None, path=None, num_col=3, figsize=None)`
Plot the frames of the video in a grid.

#### Parameters

+ **video** : *numpy.ndarray*  
    A video (numpy array) of shape `(<No. of frames>, <height>, <width>, <channels>)`, 
    which will be plotted as a grid.

+ **path** : *str*  
    The path of the video to be plotted.  
    Either pass the path of the video, or the video itself.  
    If both are passed, the one for which the path is provided will be used.

+ **num_col** : *int*, optional  
    The number of columns the grid should have, defaults to 3.

+ **figsize** : *tuple*, optional  
    The size of the entire figure, defaults to `None`.  
    This tuple is passed to the `matplotlib.figure` object to set it's size.  
    If set as `None`, it is calculated automatically (recommended).
