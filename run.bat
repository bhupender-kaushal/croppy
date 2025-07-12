@echo off
REM Windows batch script to run Image Viewer & Cropper
REM Handles Windows-specific setup and dependency checking

echo Image Viewer ^& Cropper - Windows Startup
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.6 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Warning: pip is not available
    echo You may need to install dependencies manually
)

REM Install dependencies if requirements.txt exists
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Run the application
echo Starting Image Viewer ^& Cropper...
python run.py

REM Pause if there's an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
