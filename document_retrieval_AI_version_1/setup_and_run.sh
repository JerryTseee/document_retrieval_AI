#!/bin/bash

echo "Setting up PDF Document Matcher with ChatGPT integration..."

# Create necessary directories
mkdir -p uploads
mkdir -p database
mkdir -p output

echo ""
echo "Installing Python dependencies..."
pip install Flask Flask-CORS PyPDF2 Werkzeug openai python-dotenv

echo ""
echo "Setup complete!"
echo ""
echo "To enable ChatGPT integration:"
echo "1. Rename .env.example to .env"
echo "2. Edit .env
