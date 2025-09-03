@echo off
REM ShazamIO Telegram Bot Startup Script for Windows
REM This script helps you run the bot easily on Windows

echo 🎵 ShazamIO Telegram Bot Startup Script
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not installed. Please install pip first.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Check if config.py exists and has been configured
if not exist "config.py" (
    echo ⚙️  Configuration file not found. Running setup...
    python setup.py
) else (
    REM Check if bot token is still the default
    findstr /C:"YOUR_TELEGRAM_BOT_TOKEN_HERE" config.py >nul
    if not errorlevel 1 (
        echo ⚙️  Bot token not configured. Running setup...
        python setup.py
    ) else (
        echo ✅ Configuration found.
    )
)

REM Run the bot
echo 🚀 Starting the bot...
python bot.py

pause