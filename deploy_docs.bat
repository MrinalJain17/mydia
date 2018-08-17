@echo off

cd docs

echo Deleting old documentation...
call make clean
rmdir files /S /Q
rmdir source\auto_examples /S /Q
git worktree prune
rmdir .git\worktrees\files /S /Q

echo Checking out gh-pages branch into files...
git worktree add -B gh-pages files origin/gh-pages

echo Removing existing files...
rmdir files\doctrees /S /Q
rmdir files\html /S /Q
del files\index.html
del files\.nojekyll

echo Generating site...
call make html
copy index.html .\files
copy .nojekyll .\files

echo Updating gh-pages branch...
cd files && git add --all && git commit -m "Publishing to gh-pages"
