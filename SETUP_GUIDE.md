# 🎵 ShazamIO Telegram Bot - Complete Setup Guide

## 📋 Overview

I've created a complete ShazamIO Telegram Bot with all the features you requested! Here's what's included:

### ✅ Features Implemented

1. **🎵 Music Recognition**: Identify songs from audio files using ShazamIO
2. **🌐 Language Selection**: Support for both English and Persian (فارسی)
3. **🔍 Inline Mode**: Search and share music directly in chats and channels
4. **📱 Complete Commands**: Full command set for all bot features
5. **⚙️ Easy Setup**: Interactive configuration script
6. **🛠 Advanced Features**: Rate limiting, logging, admin mode, and more

## 📁 Files Created

### Core Files
- **`bot.py`** - Main bot application with all features
- **`config.py`** - Configuration file with all settings
- **`setup.py`** - Interactive setup script
- **`requirements.txt`** - Python dependencies
- **`README.md`** - Complete documentation

### Startup Scripts
- **`start.sh`** - Linux/macOS startup script
- **`start.bat`** - Windows startup script

## 🚀 Quick Start

### Step 1: Get Your Bot Token
1. Go to [@BotFather](https://t.me/BotFather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the bot token

### Step 2: Run Setup
```bash
# Linux/macOS
python setup.py

# Or use the startup script
./start.sh

# Windows
python setup.py
# or
start.bat
```

### Step 3: Configure Bot
The setup script will ask for:
- **Bot Token**: Paste your Telegram bot token
- **Bot Username**: Your bot's username (without @)
- **Language**: Default language (English/Persian)
- **Features**: Enable/disable specific features
- **Rate Limits**: Configure request limits
- **Admin Settings**: Set up admin users (optional)

### Step 4: Run the Bot
```bash
# After setup, run the bot
python bot.py
```

## 🎯 Key Features

### 1. Audio Recognition
- Send any audio file (MP3, WAV, OGG, M4A, FLAC)
- Supports voice messages
- Maximum file size: 20MB (configurable)
- High accuracy using Shazam's technology

### 2. Inline Mode
- Use in any chat: `@bot_username [song name]`
- Example: `@ShazamIOBot Bohemian Rhapsody`
- Rich results with streaming links
- Works in groups and channels

### 3. Language Support
- **English**: Complete English interface
- **Persian (فارسی)**: Full Persian translation
- Switch anytime with `/language` command
- Persistent user preferences

### 4. Commands Available
```
/start    - Welcome message and features
/help     - Help information
/about    - About the bot
/language - Change language
/track    - Search for a track
/artist   - Search for an artist
/charts   - View global music charts
```

### 5. Advanced Features
- **Rate Limiting**: Prevents abuse
- **Admin Mode**: Optional admin-only features
- **Logging**: Comprehensive error logging
- **Database**: Optional user data persistence
- **Error Handling**: User-friendly error messages

## ⚙️ Configuration

The bot is highly configurable through `config.py`:

### Bot Settings
```python
TELEGRAM_BOT_TOKEN = "your_token_here"
BOT_USERNAME = "YourBotUsername"
DEFAULT_LANGUAGE = "en"  # or "fa"
```

### Feature Toggles
```python
ENABLE_AUDIO_RECOGNITION = True
ENABLE_INLINE_MODE = True
ENABLE_LANGUAGE_SELECTION = True
ENABLE_TRACK_INFO = True
ENABLE_ARTIST_INFO = True
ENABLE_CHARTS = True
```

### Rate Limiting
```python
ENABLE_RATE_LIMITING = True
MAX_REQUESTS_PER_MINUTE = 30
MAX_AUDIO_FILE_SIZE = 20 * 1024 * 1024  # 20MB
```

## 🎨 Welcome Message

The bot sends a comprehensive welcome message after `/start`:

**English Version:**
```
🎵 Welcome to ShazamIO Bot!

I can help you identify and find music using Shazam's powerful technology.

🔧 **Main Features:**
• Send me an audio file to identify the song
• Use inline mode in chats: @bot_username [song name]
• Get detailed information about tracks and artists
• View trending music charts worldwide
• Support for multiple languages

🌐 **Available Commands:**
/start - Show this welcome message
/language - Change bot language
/help - Show help information
/about - About this bot

🎼 **Inline Mode Usage:**
In any chat, type: @bot_username [song name or artist]
Example: @bot_username Bohemian Rhapsody

Let's find some amazing music! 🎶
```

**Persian Version:**
```
🎵 به ربات ShazamIO خوش آمدید!

من می‌توانم به شما در شناسایی و پیدا کردن موسیقی با استفاده از تکنولوژی قدرتمند شازمام کمک کنم.

🔧 **قابلیت‌های اصلی:**
• یک فایل صوتی برای من ارسال کنید تا آهنگ را شناسایی کنم
• از حالت اینلاین در چت‌ها استفاده کنید: @bot_username [نام آهنگ]
• دریافت اطلاعات دقیق درباره آهنگ‌ها و هنرمندان
• مشاهده چارت‌های موسیقی محبوب در سراسر جهان
• پشتیبانی از چندین زبان

🌐 **دستورات موجود:**
/start - نمایش این پیام خوش‌آمدگویی
/language - تغییر زبان ربات
/help - نمایش راهنما
/about - درباره این ربات

🎼 **نحوه استفاده از حالت اینلاین:**
در هر چتی، تایپ کنید: @bot_username [نام آهنگ یا هنرمند]
مثال: @bot_username Bohemian Rhapsody

بیایید موسیقی‌های فوق‌العاده‌ای پیدا کنیم! 🎶
```

## 🔧 Inline Mode Usage

The inline mode allows users to search for music directly in any chat or channel:

### How to Use:
1. In any chat or channel, type: `@bot_username [search query]`
2. Examples:
   - `@ShazamIOBot Queen`
   - `@ShazamIOBot Bohemian Rhapsody`
   - `@ShazamIOBot rap music`
3. Select a result from the search results
4. The bot will send the track information to the chat

### Features:
- **Rich Results**: Includes track info, artist, and streaming links
- **Fast Search**: Real-time search using Shazam's database
- **Universal**: Works in all chats, groups, and channels
- **No Installation**: Users don't need to add the bot to chats

## 🛠 Troubleshooting

### Common Issues:
1. **Bot Token Error**: Make sure to replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` in `config.py`
2. **Inline Mode Not Working**: Enable inline mode in @BotFather
3. **Audio Recognition Fails**: Try clearer audio or different formats
4. **Rate Limiting**: Wait a minute between requests

### Getting Help:
- Check `README.md` for detailed documentation
- Run `python setup.py` to reconfigure
- Check `bot.log` for error messages

## 🎉 Next Steps

1. **Run Setup**: `python setup.py`
2. **Configure**: Enter your bot token and preferences
3. **Test**: Send an audio file to test recognition
4. **Try Inline**: Use `@bot_username [song name]` in a chat
5. **Customize**: Edit `config.py` for advanced settings

## 📞 Support

If you need help:
1. Check the `README.md` file
2. Review the configuration in `config.py`
3. Check the logs in `bot.log`
4. Run the setup script again if needed

---

🎵 **Your ShazamIO Telegram Bot is ready to use!** 🎵

Enjoy identifying and sharing music with your new bot!