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

The program uses `Scikit-video <http://www.scikit-video.org/stable/>`__, which requires 
``FFmpeg`` to be installed on the system. To install ``FFmpeg`` on your machine - 

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

Several libraries like `Numpy <http://www.numpy.org/>`__,
`Pillow <https://python-imaging.github.io/>`__ and
`Matplotlib <https://matplotlib.org/>`__, required for the package come
pre-installed with the Anaconda distribution for Python. If you are not
using the default anaconda distribution, then first install the packages
mentioned above and along with their dependencies.

Also, install the following additional packages:

-  `Scikit-video <http://www.scikit-video.org/stable/>`__

.. code:: bash

       pip install sk-video

-  `tqdm <https://pypi.python.org/pypi/tqdm#installation>`__ - Required
   for displaying the progress bar.

.. code:: bash

       pip install tqdm
