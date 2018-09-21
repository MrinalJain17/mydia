Mydia
=====

Reading videos into NumPy arrays was never more simple. This library provides 
an entire range of additional functionalities such as custom frame selection, 
frame resizing, pixel normalization, grayscale conversion and much more.

`Read the Documentation <https://mrinaljain17.github.io/mydia/>`__

Getting started
---------------

**How to simply read a video, given its path?**

.. code:: python

   # Import
   from mydia import Videos
   
   # Initialize video path
   video_path = r".docs/examples/sample_video/bigbuckbunny.mp4"
   
   # Create a reader object
   reader = Videos()
   
   # Call the 'read()' function to get the video tensor
   # which will be of shape (1, 132, 720, 1080, 3)
   video = reader.read(video_path)

The tensor can be interpreted as -

* 1 video
* Having 132 frames, 
* Dimension (width x height) of each frame: 1080x720 pixels
* ``3`` denotes that the video is RGB

View more examples `here <https://mrinaljain17.github.io/mydia/html/auto_examples/index.html>`_
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installation
------------

-  **Install Mydia from PyPI (recommended):**

   .. code:: bash

      pip install mydia

-  **Alternatively, install from Github source:**

   First, clone the repository.

   .. code:: bash

      git clone https://github.com/MrinalJain17/mydia.git

   Then, build the module

   .. code:: bash

      cd mydia
      python setup.py install

Requirements
------------

``Python 3.x`` (preferably from the `Anaconda
Distribution <https://www.anaconda.com/download/>`__)

The program uses `ffmpeg-python <https://github.com/kkroening/ffmpeg-python>`__, which provides
python bindings for `FFmpeg <https://www.ffmpeg.org/>`__ (used as the backend for reading and 
processing videos)

To install ``FFmpeg`` on your machine - 

For **Linux** users:

   .. code:: bash
   
      $ sudo apt-get update
      $ sudo apt-get install libav-tools
   
For **Windows or MAC/OSX** users:

   Download the required binaries from
   `here <https://www.ffmpeg.org/download.html>`__. Extract the zip file
   and add the location of binaries to the ``PATH`` variable

Additional Libraries to install:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install the following packages along with their dependencies:

* `ffmpeg-python <https://github.com/kkroening/ffmpeg-python>`__
* `Numpy <http://www.numpy.org/>`__
* `tqdm <https://pypi.python.org/pypi/tqdm#installation>`__ - Required for displaying the 
  progress bar.
* `Matplotlib <https://matplotlib.org/>`__ - (Optional) For plotting the frames of a video

.. code:: bash

       pip install ffmpeg-python numpy tqdm matplotlib
