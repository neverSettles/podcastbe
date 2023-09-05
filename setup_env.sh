#!/bin/bash

# Creating virtual environment
python3 -m venv podenv

# Activating the environment
source podenv/bin/activate

# Check if requirements.txt file exists
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. Installing requirements."
    pip3 install -r requirements.txt
    sudo yum install epel-release
    sudo yum install ffmpeg ffmpeg-devel
else
    echo "No requirements.txt file found."
fi
