#!/bin/bash

# ShazamIO Telegram Bot Startup Script
# This script helps you run the bot easily

echo "🎵 ShazamIO Telegram Bot Startup Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if config.py exists and has been configured
if [ ! -f "config.py" ]; then
    echo "⚙️  Configuration file not found. Running setup..."
    python setup.py
else
    # Check if bot token is still the default
    if grep -q "YOUR_TELEGRAM_BOT_TOKEN_HERE" config.py; then
        echo "⚙️  Bot token not configured. Running setup..."
        python setup.py
    else
        echo "✅ Configuration found."
    fi
fi

# Run the bot
echo "🚀 Starting the bot..."
python bot.py