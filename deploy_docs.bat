@echo off
:: -----------------ONLY MEANT FOR INTERNAL USAGE-----------------

:: This batch file should be executed from the root of the project
cd docs

echo Deleting old documentation...
call make clean-cache
rmdir files /S /Q
rmdir ..\.git\worktrees\files /S /Q
git worktree prune

echo Checking out gh-pages branch into files...
git worktree add -B gh-pages files origin/gh-pages

echo Removing existing files...
rmdir files\doctrees /S /Q
rmdir files\html /S /Q
del files\index.html
del files\.nojekyll

echo Generating site...
call make html
copy copy\index.html .\files
copy copy\.nojekyll .\files

echo Updating gh-pages branch...
if "%~1" == "" (
	cd files && git add --all && git commit -m "Publishing docs"
) else (
	cd files && git add --all && git commit -m %1
)

echo Push changes to github
git push origin gh-pages

cd ..\..
