# ---------------------------------For internal use only----------------------------------

version="2.1.1"

conda-build mydia --numpy 1.14 -c mrinaljain17 --output-folder ./dump/mydia && cd ./dump/mydia && 
conda convert --platform win-64 "./linux-64/mydia-$version-py36h5ca1d4c_0.tar.bz2" -o . && 
conda convert --platform osx-64 "./linux-64/mydia-$version-py36h5ca1d4c_0.tar.bz2" -o . && 
anaconda upload "./linux-64/mydia-$version-py36h5ca1d4c_0.tar.bz2" && 
anaconda upload "./win-64/mydia-$version-py36h5ca1d4c_0.tar.bz2" && 
anaconda upload "./osx-64/mydia-$version-py36h5ca1d4c_0.tar.bz2" && conda-build purge
