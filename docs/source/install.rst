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
~~~~~~~~~~~~

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

-  `ffmpeg-python <https://github.com/kkroening/ffmpeg-python>`__

.. code:: bash

       pip install ffmpeg-python

-  `Numpy <http://www.numpy.org/>`__

.. code:: bash

       pip install numpy

-  `tqdm <https://pypi.python.org/pypi/tqdm#installation>`__ - Required
   for displaying the progress bar.

.. code:: bash

       pip install tqdm

-  `Matplotlib <https://matplotlib.org/>`__ - (Optional) For plotting the frames
   of a video

.. code:: bash

       pip install matplotlib
