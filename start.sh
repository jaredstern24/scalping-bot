#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting scalping bot..."
python main.py
