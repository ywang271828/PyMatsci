#!/bin/bash

python -m pip install --upgrade --user pip build setuptools
python -m build
python -m pip install -e .    # Development install
# For a deployment installation:
# python -m pip install --force-reinstall dist/PyMatsci-0.0.1-py3-none-any.whl
