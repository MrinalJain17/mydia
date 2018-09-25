# Mydia Documentation

The source for Mydia documentation is under the directory `source/`. 
The documentation is built using [sphinx](http://www.sphinx-doc.org/en/master/) and the examples are executed while building the docs 
using [sphinx gallery](https://github.com/sphinx-gallery/sphinx-gallery).

## Building the documentation

1. Install `mydia` from source
2. Install the dependencies for docs
    ```bash
        pip install sphinx sphinx-gallery
    ```
3. Run the following command from the root of the repository:
    ```bash
        cd docs
        make docs
    ```

The docs will be built in the directory `files/`.
