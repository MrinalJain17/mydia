@echo off
:: ---------------------ONLY MEANT FOR INTERNAL USAGE---------------------

:: This file should be executed inside the `docs` directory of the project
echo Deleting old documentation...
call make clean-cache
PowerShell -Command "rm -r -force files"
PowerShell -Command "rm -r -force ../.git/worktrees/html"
git worktree prune

echo Checking out gh-pages branch...
mkdir files
git worktree add -B gh-pages files/html origin/gh-pages

echo Removing existing files...
PowerShell -Command "rm -r files/html/*"

echo Generating site...
call make html
call>files/html/.nojekyll

echo Updating gh-pages branch...
cd files/html && git add --all 
if "%~1" == "" (
	git commit -m "Publishing docs"
) else (
	git commit -m %1
)

echo Push changes to github
git push origin gh-pages

cd ../..
