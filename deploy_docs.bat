@echo off

cd docs

echo "Deleting old documentation"
make clean
rmdir files /S /Q
rmdir source\auto_examples /S /Q
git worktree prune
rmdir .git\worktrees\files /S /Q

echo "Checking out gh-pages branch into files"
git worktree add -B gh-pages files origin/gh-pages

echo "Removing existing files"
rmdir files\doctrees /S /Q
rmdir files\html /S /Q
del index.html
del .nojekyll

echo "Generating site"
make html
copy index.html .\files
copy .nojekyll .\files

cd files && git add --all && git commit -m "Publishing to gh-pages"