#!/bin/bash
set -e # everything must succeed
if [ ! -e venv/bin/activate ]; then
    rm -rf venv/
    python -m venv venv
fi
source venv/bin/activate
pip install -r requirements.lock

