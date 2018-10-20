@echo off
:: ---------------------------------For internal use only----------------------------------

SET VERSION=4.0.2

call conda-build ffmpeg --numpy 1.14 --output-folder .\dump\ffmpeg
call anaconda upload "./dump/ffmpeg/win-64/ffmpeg-%version%-0.tar.bz2"
call conda build purge
rd /S /Q dump
