#!/bin/bash

python -m pip install --upgrade --user pip build setuptools
python -m build
python -m pip install --force-reinstall dist/pyMatsci-0.0.1-py3-none-any.whl