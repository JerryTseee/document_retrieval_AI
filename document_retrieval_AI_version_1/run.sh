#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads
mkdir -p database

echo "Setup complete! Now run:"
echo "python app.py"
echo ""
echo "Then open your browser to: http://localhost:5000"
