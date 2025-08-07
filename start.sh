#!/bin/bash

echo "Installing dependencies..."
pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "Starting scalping bot..."
python3 main.py
