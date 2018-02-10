## `Videos`

To read in videos and store them as NumPy arrays.

The videos are stored as a 5-dimensional tensor - `(<No. of Videos>, <No. of frames>, <height>, <width>, <channels>)`.  
The value of `channels` could be 1 (gray scale) or 3 (RGB).

- **`target_size (tuple)`**: `(New_Width, New_Height)`. Defaults to `None`.
A tuple denoting the target width and height (of the frames) of the videos.
If not set, the dimensions of the frames will not be altered.

	**Note:**  
		A single video is a stack of frames. If the dimension of all the frames is not the same, they cannot by stacked.

- **`to_gray (boolean)`**: Whether to convert each video (all the frames) to gray scale or not. Defaults to `False`.

- **`max_frames (int)`**: The (maximum) number of frames to extract from each video. Defaults to `None`.

	Frames are extracted based on the value of `extract_frames`.

	If not set, all the frames would be kept.

	**Note:**  
		Videos are stacked together. If the number of frames in all the videos are not the same, they cannot be stacked.

- **`extract_frames (str)`**: **{'first', 'middle', 'last'}**. Defaults to `'middle'`.

	*'first'*: Extract the frames from the beginning of the video. 
 
	*'last'*: Extract the frames from the end of the video.  

	*'middle'*: Extract the frames from the middle of the video.  

	Removes `((total frames - 'max_frames') // 2)` from the beginning ant the end of the video.

- **`required_fps (int)`**: The number of frame(s) to capture per second from the video. Defaults to `None`.  

	For each second of the video, only the first *'N'* frames are captured.  

	If set to `0`, then the value of this parameter is *adaptive to each video*.
	It will extract exactly `max_frames` frames from each of the video (of any duration).
	
	- E.g. Let the duration of a video to be 10 seconds assume it was captured at the rate of *30fps*.  
		Suppose the value of `required_fps` is set to 7.  
		Then, for each second, the first 7 frames would be captured.  
		The resulting video (in form of tensor) will have a total of _10 * 7 = 70 frames_.  
	
- **`normalize_pixels (tuple, str)`**: Whether to normalize pixel values for each video or not. Defaults to `None`.  
	The pixel values would be normalized based on the pixels of each video.

	**tuple** - `(New_min, New_max)`: Min-max normalization will be used.  

	**str** - `'z-score'`: Z-score normalization will be used.  

	If not set, then the pixels would not be normalized.  

### `read_videos(paths)`

Function to read videos.

#### **Args**:
- `paths (list of str)`: A list of paths of the videos to be read.

#### **Returns**:
- Numpy.ndarray: A 5-dimensional tensor with shape `(<No. of Videos>, <No. of frames>, <height>, <width>, <channels>)`.  
The value of `channels` could be 1 (gray scale) or 3 (RGB).

#### **Raises**:
- `ValueError`: If the value of `normalize_pixels` is invalid.

### `get_frame_count(paths)`

Get the number of frames of all the videos.

Can be used to determine the value of `max_frames`.

#### **Args**:
- `paths (list of str)`: A list of paths of the videos to be read.

#### **Returns**:
- `dict (python dictionary)`: Key - *path of video*, value - *number of frames in that video*.