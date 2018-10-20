@echo off
:: This code is taken from https://github.com/menpo/conda-ffmpeg/blob/master/conda/bld.bat
rd /S /Q %SCRIPTS%
mkdir %SCRIPTS%

SET VERSION=4.0.2

copy ".\bin\ffmpeg.exe" "%SCRIPTS%\ffmpeg.exe"
copy ".\bin\ffplay.exe" "%SCRIPTS%\ffplay.exe"
copy ".\bin\ffprobe.exe" "%SCRIPTS%\ffprobe.exe"

if errorlevel 1 exit 1
