@echo off
echo Setting up PDF Document Matcher with ChatGPT integration...

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "database" mkdir database
if not exist "output" mkdir output

echo.
echo Installing Python dependencies...
pip install Flask Flask-CORS PyPDF2 Werkzeug openai python-dotenv

echo.
echo Setup complete!
echo.
echo To enable ChatGPT integration:
echo 1. Rename .env.example to .env
echo 2. Edit .env and add your OpenAI API key
echo.
echo Put your searchable PDF/DOCX files in the 'database' folder
echo.
echo Starting Flask server...
python app.py

pause
