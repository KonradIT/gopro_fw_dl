#!/bin/bash
set -e # everything must succeed
if [ ! -e venv-py2/bin/activate ]; then
    rm -rf venv-py2/
    virtualenv venv-py2 --python=$(which python2)
fi
source venv-py2/bin/activate
pip install -r requirements.lock

