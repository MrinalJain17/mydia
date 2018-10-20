# ---------------------------------For internal use only----------------------------------

version="4.0.2"

conda-build ffmpeg --numpy 1.14 --output-folder ./dump/ffmpeg && cd ./dump/ffmpeg && 
conda convert --platform osx-64 "./linux-64/ffmpeg-$version-0.tar.bz2" -o . && 
anaconda upload "./linux-64/ffmpeg-$version-0.tar.bz2" &&  
anaconda upload "./osx-64/ffmpeg-$version-0.tar.bz2" && conda-build purge
