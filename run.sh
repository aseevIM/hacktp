#!/bin/bash

pip install -r requirements.txt

python3 src/main.py --inbox ./inbox --output ./sorted "$@"
