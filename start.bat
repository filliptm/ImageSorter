@echo off
echo Starting ImageSorter...

REM Check if venv directory exists
if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    
    echo Installing requirements...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo Setup complete!
) else (
    echo Virtual environment found.
    call venv\Scripts\activate.bat
)

echo Launching ImageSorter...
python app.py

REM Keep the window open if there's an error
if %ERRORLEVEL% neq 0 (
    echo An error occurred while running the application.
    pause
)