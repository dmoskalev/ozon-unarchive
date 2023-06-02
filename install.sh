#!/bin/sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Virtual environment created and activated. Dependencies installed."
