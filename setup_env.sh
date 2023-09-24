#!/bin/bash

# Creating virtual environment
python3 -m venv podenv

# Activating the environment
source podenv/bin/activate

# Check if requirements.txt file exists
if [ -f "requirements.txt" ]; then
    echo "requirements.txt found. Installing requirements."
    pip3 install -r requirements.txt
    sudo apt update
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
    tar xf ffmpeg-release-amd64-static.tar.xz
    cd ffmpeg-*-amd64-static/
    sudo cp ffmpeg /usr/local/bin/
else
    echo "No requirements.txt file found."
fi
