from codecs import open
from os import path

from setuptools import find_packages, setup

from mydia import mydia

# Get the long description from the README file
with open("README.rst", encoding="utf-8") as f:
    long_description = f.read()
    long_description = long_description.replace("\r", "")

setup(
    name="mydia",
    version=mydia.__version__,
    description="Read videos as numpy arrays",
    long_description=long_description,
    url="https://mrinaljain17.github.io/mydia/",
    author="Mrinal Jain",
    author_email="mrinaljain007@gmail.com",
    license="MIT",
    install_requires=["numpy>=1.14.5", "ffmpeg-python>=0.1.16", "tqdm>=4.25.0"],
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
    packages=find_packages(),
    project_urls={
        "Documentation": "https://mrinaljain17.github.io/mydia/",
        "Source": "https://github.com/MrinalJain17/mydia",
    },
)
