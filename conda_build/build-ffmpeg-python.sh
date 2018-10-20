# ---------------------------------For internal use only----------------------------------

version="0.1.16"

conda-build ffmpeg-python --numpy 1.14 --output-folder ./dump/ffmpeg_python && cd ./dump/ffmpeg_python && 
conda convert --platform win-64 "./linux-64/ffmpeg-python-$version-py36_0.tar.bz2" -o . && 
conda convert --platform osx-64 "./linux-64/ffmpeg-python-$version-py36_0.tar.bz2" -o . && 
anaconda upload "./linux-64/ffmpeg-python-$version-py36_0.tar.bz2" && 
anaconda upload "./win-64/ffmpeg-python-$version-py36_0.tar.bz2" && 
anaconda upload "./osx-64/ffmpeg-python-$version-py36_0.tar.bz2" && conda-build purge
