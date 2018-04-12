from setuptools import find_packages, setup

setup(
    name="Mydia",
    version="1.0.0",
    description="Reding videos as NumPy arrays",
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
)
