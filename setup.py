from setuptools import find_packages, setup
from codecs import open
from os import path

here = path.abspath(path.dirname("."))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="Mydia",
    version="1.0.1",
    description="Read videos as numpy arrays",
    long_description=long_description,
    long_description_content_type="text/markdown; charset=UTF-8; variant=GFM",
    url="https://mrinaljain17.github.io/Mydia/",
    author="Mrinal Jain",
    author_email="mrinaljain007@gmail.com",
    license="MIT",
    install_requires=[
        "numpy>=1.14.2",
        "matplotlib>=2.2.2",
        "Pillow>=5.1.0",
        "sk-video>=1.1.10",
        "tqdm>=4.20.0",
    ],
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
        "Documentation": "https://mrinaljain17.github.io/Mydia/",
        "Bug Reports": "https://github.com/MrinalJain17/Mydia/issues",
        "Source": "https://github.com/MrinalJain17/Mydia",
    },
)
