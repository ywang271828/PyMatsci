#!/bin/bash

python -m pip install --upgrade --user pip build setuptools
python -m build
python -m pip install --prefix=~/.local -e .
# The --user option causes a bizzare problem which pertains for more than a year
# now. Check: https://github.com/pypa/pip/issues/7953
# A workaround is to use --prefix=~/.local instead of --user.
# python -m pip install --user -e .    # Development install

# For a deployment installation:
# python -m pip install --force-reinstall dist/PyMatsci-0.0.1-py3-none-any.whl
