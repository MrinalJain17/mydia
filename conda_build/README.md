# Conda Package Manager

Run the following commands from the directory `conda_build/` to build conda distribution 
of the package:

```bash
pip install conda-build
conda-build mydia --numpy 1.14 -c mrinaljain17
```

Here, `"mrinaljain17"` is the channel from which `ffmpeg-python` is installed.
