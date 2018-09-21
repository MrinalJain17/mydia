@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=files
set SPHINXPROJ=Mydia

if "%1" == "" goto help

if "%1" == "clean-cache" (
	%SPHINXBUILD% -M clean %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
	echo.Removing everything under 'auto_examples'...
	rd /s /q %SOURCEDIR%\auto_examples\
	goto end
)

if "%1" == "html-noplot" (
	%SPHINXBUILD%  -D plot_gallery=0 -b html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
	echo
	echo.Build finished.
	goto end
)

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%

:end
popd
