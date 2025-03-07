#!/bin/bash

source ./venv/bin/activate
nohup python app.py > app.log 2>&1 &

