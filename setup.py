import io
import os

from setuptools import find_packages, setup

from mydia.mydia import __version__

NAME = "mydia"
DESCRIPTION = "A simple and efficient wrapper for reading videos as NumPy tensors."
URL = "https://mrinaljain17.github.io/mydia/"
DOCS = "https://mrinaljain17.github.io/mydia/"
AUTHOR = "Mrinal Jain"
EMAIL = "mrinaljain007@gmail.com"
VERSION = __version__

REQUIRED = ["numpy>=1.14.5", "ffmpeg-python>=0.1.16", "tqdm>=4.25.0"]

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()
    long_description = long_description.replace("\r", "")

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    license="MIT",
    install_requires=REQUIRED,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "numpy"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video :: Capture",
    ],
    packages=find_packages(exclude=("tests",)),
    project_urls={"Documentation": DOCS, "Source": URL},
)
