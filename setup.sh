#!/bin/bash

echo "Setting up Predictive Maintenance System..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir -p models logs data

# Initialize database
python db_init.py

echo "Setup completed!"