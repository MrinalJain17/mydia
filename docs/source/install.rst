Setup
=====

Requirements
------------

- Python 3.x (preferably from the `Anaconda Distribution <https://www.anaconda.com/download/>`__)
- `FFmpeg <https://www.ffmpeg.org/>`__: The backend for reading and processing videos.
  
  The recommended (and probably the easiest) way of installing ``FFmpeg`` is 
  via the conda package manager.

  .. code:: bash

      conda install -c mrinaljain17 ffmpeg
    
  However, if you are not using *conda*, then
  
  For **Linux** users:
  
     .. code:: bash
     
        $ sudo apt-get update
        $ sudo apt-get install ffmpeg
     
  For **Windows or OSX** users:
  
     Download the required binaries from `here <https://www.ffmpeg.org/download.html>`__. 
     Extract the zip file and add the location of binaries to the ``PATH`` variable.

Installation
------------

1. **Using the conda package manager (recommended):**

   .. code:: bash

      conda install -c mrinaljain17 mydia

2. **Using pip:**

   .. code:: bash

      pip install mydia

The following python packages that ``mydia`` depends on, will also be installed, 
along with their dependencies.

- `ffmpeg-python <https://github.com/kkroening/ffmpeg-python>`__
- `NumPy <http://www.numpy.org/>`__
- `tqdm <https://pypi.python.org/pypi/tqdm#installation>`__ - Required for displaying the 
  progress bar.
