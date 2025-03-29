#!/bin/bash

# Navigate to the src directory
cd src

# Activate the virtual environment
source .venv/bin/activate

# Start the Flask application
flask run --host=0.0.0.0 --port=8000