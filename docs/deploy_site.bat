@echo off

:: Generate site
hugo

:: Commit changes to gh-pages
cd public && git add --all && git commit -m "Publishing to gh-pages" && cd ..