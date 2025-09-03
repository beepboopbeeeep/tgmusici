# 🎵 ShazamIO Telegram Bot

A powerful music identification and search bot for Telegram built with ShazamIO library. This bot can identify songs from audio files, search for music, and provide detailed information about tracks and artists.

## ✨ Features

### 🎵 Music Identification
- **Audio File Recognition**: Send any audio file (MP3, WAV, OGG, M4A, FLAC) to identify the song
- **Voice Message Support**: Recognize music from voice messages
- **High Accuracy**: Uses Shazam's powerful recognition technology

### 🔍 Music Search
- **Track Search**: Search for specific songs by name
- **Artist Search**: Find information about artists
- **Inline Mode**: Search and share music directly in chats and channels
- **Global Charts**: View trending music worldwide

### 🌐 Multi-Language Support
- **English**: Full English language support
- **Persian (فارسی)**: Complete Persian language interface
- **Dynamic Language Switching**: Change language anytime with /language command

### 🎯 Inline Mode
- **Chat Integration**: Use the bot directly in any chat or channel
- **Quick Search**: Type `@bot_username [song name]` to search
- **Rich Results**: Get detailed track information with streaming links

### 🛠 Advanced Features
- **Rate Limiting**: Prevents abuse with configurable limits
- **Admin Mode**: Optional admin-only features
- **Logging**: Comprehensive logging for debugging
- **Database Support**: Optional user data persistence
- **Error Handling**: Graceful error handling with user-friendly messages

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/shazamio-telegram-bot.git
cd shazamio-telegram-bot

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

#### Option A: Interactive Setup (Recommended)

```bash
# Run the interactive setup script
python setup.py
```

This will guide you through:
- Setting up your Telegram bot token
- Configuring bot features
- Setting up language preferences
- Configuring rate limits and other options

#### Option B: Manual Configuration

1. Get your bot token from [@BotFather](https://t.me/BotFather) on Telegram
2. Edit `config.py` and replace `YOUR_TELEGRAM_BOT_TOKEN_HERE` with your actual token
3. Configure other settings as needed

### 3. Run the Bot

```bash
# Start the bot
python bot.py
```

Your bot is now running and ready to use!

## 📖 Usage Guide

### Basic Commands

| Command | Description |
|---------|-------------|
| `/start` | Show welcome message and features |
| `/help` | Display help information |
| `/about` | About the bot |
| `/language` | Change bot language (English/Persian) |
| `/track [name]` | Search for a specific track |
| `/artist [name]` | Search for an artist |
| `/charts` | View global music charts |

### Audio Recognition

1. **Send Audio File**: Simply send any audio file to the bot
2. **Supported Formats**: MP3, WAV, OGG, M4A, FLAC
3. **File Size Limit**: 20MB (configurable)
4. **Voice Messages**: Send voice messages for recognition

### Inline Mode Usage

1. **In Any Chat**: Type `@bot_username [search query]`
2. **Examples**:
   - `@ShazamIOBot Bohemian Rhapsody`
   - `@ShazamIOBot Queen`
   - `@ShazamIOBot rap`
3. **Select Result**: Choose from the search results to send to the chat

### Language Selection

1. **Change Language**: Use `/language` command
2. **Available Options**: English (🇺🇸) or Persian (🇮🇷)
3. **Persistent**: Your language preference is saved

## ⚙️ Configuration

### Key Configuration Options

```python
# Bot Configuration
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
BOT_USERNAME = "YourBotUsername"
DEFAULT_LANGUAGE = "en"  # or "fa"

# Feature Flags
ENABLE_AUDIO_RECOGNITION = True
ENABLE_INLINE_MODE = True
ENABLE_LANGUAGE_SELECTION = True
ENABLE_TRACK_INFO = True
ENABLE_ARTIST_INFO = True
ENABLE_CHARTS = True

# Rate Limiting
ENABLE_RATE_LIMITING = True
MAX_REQUESTS_PER_MINUTE = 30
MAX_AUDIO_FILE_SIZE = 20 * 1024 * 1024  # 20MB
```

### Advanced Configuration

The bot supports extensive customization through `config.py`:

- **Admin Settings**: Configure admin users and admin-only mode
- **Logging**: Set log levels and file logging
- **Database**: Enable SQLite database for user data persistence
- **Rate Limiting**: Configure request limits per user
- **Feature Toggles**: Enable/disable specific features

## 🛠 Development

### Project Structure

```
shazamio-telegram-bot/
├── bot.py              # Main bot application
├── config.py           # Configuration file
├── setup.py            # Interactive setup script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── bot.log            # Log file (created when running)
```

### Dependencies

- **python-telegram-bot**: Telegram Bot API wrapper
- **shazamio**: Shazam API client for Python
- **aiohttp**: Async HTTP client
- **dataclasses-json**: Data serialization
- **asyncio-throttle**: Rate limiting

### Running in Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run the bot
python bot.py

# Enable debug logging (edit config.py):
LOG_LEVEL = "DEBUG"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Bot Token Error
```
❌ Error: Please set your Telegram bot token in config.py
```
**Solution**: Get your token from [@BotFather](https://t.me/BotFather) and update `config.py`

#### 2. Audio Recognition Fails
```
❌ Sorry, I couldn't identify this audio
```
**Solutions**:
- Ensure the audio is clear and contains music
- Try a different audio format
- Check file size (max 20MB)
- Make sure the song exists in Shazam's database

#### 3. Inline Mode Not Working
**Solutions**:
- Enable inline mode in [@BotFather](https://t.me/BotFather)
- Check bot username in config
- Ensure `ENABLE_INLINE_MODE = True` in config

#### 4. Rate Limiting
```
⚠️ Too many requests! Please wait a moment
```
**Solution**: Wait a minute before trying again, or adjust `MAX_REQUESTS_PER_MINUTE`

### Logging

Check `bot.log` for detailed error information:
```bash
tail -f bot.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test new features thoroughly
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ShazamIO](https://github.com/shazamio/ShazamIO) for the amazing Shazam API library
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent Telegram Bot framework
- [Shazam](https://www.shazam.com/) for the music recognition service

## 📞 Support

If you encounter any issues or have questions:
1. Check this README for troubleshooting
2. Review the issue tracker on GitHub
3. Create a new issue with detailed information
4. Contact the bot admin if configured

---

🎵 **Enjoy identifying and sharing music with ShazamIO Bot!** 🎵