#!/bin/bash
set -e
./install.sh > /dev/null
source venv/bin/activate
python gopro-fw-dl.py
