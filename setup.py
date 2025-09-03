#!/usr/bin/env python3
"""
ShazamIO Telegram Bot Setup Script
This script helps you set up the bot configuration
"""

import os
import sys
import json
from typing import Dict, Any

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the setup header"""
    print("=" * 60)
    print("🎵 ShazamIO Telegram Bot Setup")
    print("=" * 60)
    print()

def get_input(prompt: str, default: str = "", required: bool = True) -> str:
    """Get user input with validation"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip() or default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if required and not user_input:
            print("❌ This field is required!")
            continue
        
        return user_input

def get_yes_no(prompt: str, default: bool = True) -> bool:
    """Get yes/no input from user"""
    default_str = "Y/n" if default else "y/N"
    while True:
        user_input = input(f"{prompt} [{default_str}]: ").strip().lower()
        
        if not user_input:
            return default
        
        if user_input in ['y', 'yes', '1']:
            return True
        elif user_input in ['n', 'no', '0']:
            return False
        
        print("❌ Please enter 'y' or 'n'")

def get_numeric_input(prompt: str, default: int, min_val: int = None, max_val: int = None) -> int:
    """Get numeric input with validation"""
    while True:
        try:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                return default
            
            value = int(user_input)
            
            if min_val is not None and value < min_val:
                print(f"❌ Value must be at least {min_val}")
                continue
            
            if max_val is not None and value > max_val:
                print(f"❌ Value must be at most {max_val}")
                continue
            
            return value
            
        except ValueError:
            print("❌ Please enter a valid number")

def setup_bot():
    """Main setup function"""
    clear_screen()
    print_header()
    
    print("📋 This setup will help you configure your ShazamIO Telegram Bot.")
    print("Please provide the following information:\n")
    
    # Bot configuration
    print("🤖 Bot Configuration:")
    bot_token = get_input("Enter your Telegram Bot Token", required=True)
    bot_username = get_input("Enter your bot username (without @)", "ShazamIOBot")
    bot_display_name = get_input("Enter your bot display name", "ShazamIO Bot")
    
    print()
    
    # Language configuration
    print("🌐 Language Configuration:")
    default_lang = get_input("Default language (en/fa)", "en")
    while default_lang not in ['en', 'fa']:
        print("❌ Please enter 'en' for English or 'fa' for Persian")
        default_lang = get_input("Default language (en/fa)", "en")
    
    enable_language_selection = get_yes_no("Enable language selection feature", True)
    
    print()
    
    # Feature configuration
    print("🔧 Feature Configuration:")
    enable_audio_recognition = get_yes_no("Enable audio file recognition", True)
    enable_inline_mode = get_yes_no("Enable inline mode for chats", True)
    enable_track_info = get_yes_no("Enable track info commands", True)
    enable_artist_info = get_yes_no("Enable artist info commands", True)
    enable_charts = get_yes_no("Enable music charts", True)
    
    print()
    
    # Rate limiting configuration
    print("⚡ Rate Limiting Configuration:")
    enable_rate_limiting = get_yes_no("Enable rate limiting", True)
    max_requests_per_minute = get_numeric_input("Max requests per user per minute", 30, 1, 100)
    
    print()
    
    # File size configuration
    print("📁 File Size Configuration:")
    max_file_size_mb = get_numeric_input("Max audio file size (MB)", 20, 1, 100)
    max_file_size_bytes = max_file_size_mb * 1024 * 1024
    
    print()
    
    # Admin configuration
    print("👤 Admin Configuration:")
    admin_mode = get_yes_no("Enable admin-only mode", False)
    admin_ids = []
    
    if admin_mode or get_yes_no("Add admin user IDs", False):
        print("Enter admin user IDs (one per line, empty line to finish):")
        while True:
            admin_id = input("Admin ID: ").strip()
            if not admin_id:
                break
            try:
                admin_ids.append(int(admin_id))
            except ValueError:
                print("❌ Please enter a valid user ID")
    
    print()
    
    # Logging configuration
    print("📝 Logging Configuration:")
    log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    print("Available log levels:", ", ".join(log_levels))
    log_level = get_input("Log level", "INFO")
    while log_level not in log_levels:
        print(f"❌ Please choose from: {', '.join(log_levels)}")
        log_level = get_input("Log level", "INFO")
    
    enable_file_logging = get_yes_no("Enable file logging", True)
    log_file = "bot.log" if enable_file_logging else ""
    
    print()
    
    # Database configuration
    print("💾 Database Configuration:")
    enable_database = get_yes_no("Enable user data persistence", False)
    database_file = "bot_data.db" if enable_database else ""
    
    print()
    
    # Show configuration summary
    print("📊 Configuration Summary:")
    print("-" * 40)
    print(f"Bot Token: {'*' * len(bot_token)}")
    print(f"Bot Username: @{bot_username}")
    print(f"Bot Display Name: {bot_display_name}")
    print(f"Default Language: {default_lang}")
    print(f"Language Selection: {'Enabled' if enable_language_selection else 'Disabled'}")
    print(f"Audio Recognition: {'Enabled' if enable_audio_recognition else 'Disabled'}")
    print(f"Inline Mode: {'Enabled' if enable_inline_mode else 'Disabled'}")
    print(f"Track Info: {'Enabled' if enable_track_info else 'Disabled'}")
    print(f"Artist Info: {'Enabled' if enable_artist_info else 'Disabled'}")
    print(f"Music Charts: {'Enabled' if enable_charts else 'Disabled'}")
    print(f"Rate Limiting: {'Enabled' if enable_rate_limiting else 'Disabled'}")
    if enable_rate_limiting:
        print(f"  Max requests/min: {max_requests_per_minute}")
    print(f"Max File Size: {max_file_size_mb}MB")
    print(f"Admin Mode: {'Enabled' if admin_mode else 'Disabled'}")
    if admin_ids:
        print(f"Admin IDs: {', '.join(map(str, admin_ids))}")
    print(f"Log Level: {log_level}")
    print(f"File Logging: {'Enabled' if enable_file_logging else 'Disabled'}")
    print(f"Database: {'Enabled' if enable_database else 'Disabled'}")
    print("-" * 40)
    
    print()
    
    # Confirm configuration
    if not get_yes_no("Save this configuration?", True):
        print("❌ Configuration cancelled.")
        return
    
    # Generate config file
    generate_config_file({
        'bot_token': bot_token,
        'bot_username': bot_username,
        'bot_display_name': bot_display_name,
        'default_language': default_lang,
        'enable_language_selection': enable_language_selection,
        'enable_audio_recognition': enable_audio_recognition,
        'enable_inline_mode': enable_inline_mode,
        'enable_track_info': enable_track_info,
        'enable_artist_info': enable_artist_info,
        'enable_charts': enable_charts,
        'enable_rate_limiting': enable_rate_limiting,
        'max_requests_per_minute': max_requests_per_minute,
        'max_file_size_bytes': max_file_size_bytes,
        'admin_mode': admin_mode,
        'admin_ids': admin_ids,
        'log_level': log_level,
        'log_file': log_file,
        'enable_database': enable_database,
        'database_file': database_file,
    })
    
    print()
    print("✅ Configuration saved successfully!")
    print()
    print("🚀 Next steps:")
    print("1. Install required dependencies: pip install -r requirements.txt")
    print("2. Run the bot: python bot.py")
    print("3. Test your bot in Telegram!")
    print()
    print("📚 For help and documentation, check the README.md file")

def generate_config_file(config: Dict[str, Any]):
    """Generate the config.py file"""
    config_content = f'''"""
Configuration file for ShazamIO Telegram Bot
Generated by setup.py on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

# =============================================
# TELEGRAM BOT CONFIGURATION
# =============================================

# Your Telegram Bot Token from @BotFather
TELEGRAM_BOT_TOKEN = "{config['bot_token']}"

# Bot username (without @)
BOT_USERNAME = "{config['bot_username']}"

# Bot display name
BOT_DISPLAY_NAME = "{config['bot_display_name']}"

# =============================================
# BOT BEHAVIOR CONFIGURATION
# =============================================

# Maximum number of results for inline queries
MAX_INLINE_RESULTS = 10

# Maximum file size for audio recognition (in bytes)
MAX_AUDIO_FILE_SIZE = {config['max_file_size_bytes']}

# Supported audio formats for recognition
SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']

# Default language (change to 'fa' for Persian or 'en' for English)
DEFAULT_LANGUAGE = "{config['default_language']}"

# =============================================
# SHAZAMIO CONFIGURATION
# =============================================

# Shazam API timeout (in seconds)
SHAZAM_TIMEOUT = 30

# Maximum retries for Shazam API calls
SHAZAM_MAX_RETRIES = 3

# =============================================
# MESSAGE TEMPLATES
# =============================================

# Bot description for inline mode
INLINE_DESCRIPTION = {{
    'en': "🎵 Find and identify music with ShazamIO Bot",
    'fa': "🎵 پیدا کردن و شناسایی موسیقی با ربات ShazamIO"
}}

# =============================================
# ADMIN CONFIGURATION
# =============================================

# Admin user IDs (optional)
ADMIN_USER_IDS = {config['admin_ids']}

# Enable admin-only features
ADMIN_ONLY_MODE = {config['admin_mode']}

# =============================================
# LOGGING CONFIGURATION
# =============================================

# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL = "{config['log_level']}"

# Log file path (leave empty to disable file logging)
LOG_FILE = "{config['log_file']}"

# =============================================
# DATABASE CONFIGURATION (Optional)
# =============================================

# Enable user data persistence
ENABLE_DATABASE = {config['enable_database']}

# Database file path (SQLite)
DATABASE_FILE = "{config['database_file']}"

# =============================================
# RATE LIMITING CONFIGURATION
# =============================================

# Enable rate limiting
ENABLE_RATE_LIMITING = {config['enable_rate_limiting']}

# Maximum requests per user per minute
MAX_REQUESTS_PER_MINUTE = {config['max_requests_per_minute']}

# =============================================
# FEATURE FLAGS
# =============================================

# Enable audio file recognition
ENABLE_AUDIO_RECOGNITION = {config['enable_audio_recognition']}

# Enable inline mode
ENABLE_INLINE_MODE = {config['enable_inline_mode']}

# Enable language selection
ENABLE_LANGUAGE_SELECTION = {config['enable_language_selection']}

# Enable track info commands
ENABLE_TRACK_INFO = {config['enable_track_info']}

# Enable artist info commands
ENABLE_ARTIST_INFO = {config['enable_artist_info']}

# Enable charts and trending
ENABLE_CHARTS = {config['enable_charts']}

# =============================================
# CUSTOMIZATION
# =============================================

# Bot about text
BOT_ABOUT_TEXT = {{
    'en': "🎵 ShazamIO Bot - Your music identification assistant!\\n\\n"
          "Features:\\n"
          "• Identify music from audio files\\n"
          "• Search for songs and artists\\n"
          "• Get track information\\n"
          "• View music charts\\n"
          "• Inline mode for chats\\n"
          "• Multi-language support",
    
    'fa': "🎵 ربات ShazamIO - دستیار شناسایی موسیقی شما!\\n\\n"
          "قابلیت‌ها:\\n"
          "• شناسایی موسیقی از فایل‌های صوتی\\n"
          "• جستجوی آهنگ‌ها و هنرمندان\\n"
          "• دریافت اطلاعات آهنگ\\n"
          "• مشاهده چارت‌های موسیقی\\n"
          "• حالت اینلاین برای چت‌ها\\n"
          "• پشتیبانی چندزبانه"
}}

# Start message templates
START_MESSAGE = {{
    'en': """🎵 Welcome to ShazamIO Bot!

I can help you identify and find music using Shazam's powerful technology.

🔧 **Main Features:**
• Send me an audio file to identify the song
• Use inline mode in chats: @{bot_username} [song name]
• Get detailed information about tracks and artists
• View trending music charts worldwide
• Support for multiple languages

🌐 **Available Commands:**
/start - Show this welcome message
/language - Change bot language
/help - Show help information
/about - About this bot

🎼 **Inline Mode Usage:**
In any chat, type: @{bot_username} [song name or artist]
Example: @{bot_username} Bohemian Rhapsody

Let's find some amazing music! 🎶""",
    
    'fa': """🎵 به ربات ShazamIO خوش آمدید!

من می‌توانم به شما در شناسایی و پیدا کردن موسیقی با استفاده از تکنولوژی قدرتمند شازمام کمک کنم.

🔧 **قابلیت‌های اصلی:**
• یک فایل صوتی برای من ارسال کنید تا آهنگ را شناسایی کنم
• از حالت اینلاین در چت‌ها استفاده کنید: @{bot_username} [نام آهنگ]
• دریافت اطلاعات دقیق درباره آهنگ‌ها و هنرمندان
• مشاهده چارت‌های موسیقی محبوب در سراسر جهان
• پشتیبانی از چندین زبان

🌐 **دستورات موجود:**
/start - نمایش این پیام خوش‌آمدگویی
/language - تغییر زبان ربات
/help - نمایش راهنما
/about - درباره این ربات

🎼 **نحوه استفاده از حالت اینلاین:**
در هر چتی، تایپ کنید: @{bot_username} [نام آهنگ یا هنرمند]
مثال: @{bot_username} Bohemian Rhapsody

بیایید موسیقی‌های فوق‌العاده‌ای پیدا کنیم! 🎶"""
}}

# Help message templates
HELP_MESSAGE = {{
    'en': """🎵 **ShazamIO Bot Help**

🔧 **How to use me:**

**1. Audio Recognition:**
• Send me any audio file (MP3, WAV, OGG, M4A, FLAC)
• I'll identify the song and provide detailed information

**2. Inline Mode:**
• In any chat, type: @{bot_username} [search query]
• Example: @{bot_username} Queen Bohemian Rhapsody
• Select a result to send it to the chat

**3. Search Commands:**
• /track [song name] - Search for a specific track
• /artist [artist name] - Search for an artist
• /charts - View global music charts
• /top [country] - Top tracks in a country

**4. Language:**
• /language - Change bot language (English/Persian)

📝 **Tips:**
• Maximum file size: {config['max_file_size_bytes'] // (1024*1024)}MB
• Supported formats: MP3, WAV, OGG, M4A, FLAC
• Inline mode works in all chats and channels

Need more help? Contact @admin""",
    
    'fa': """🎵 **راهنمای ربات ShazamIO**

🔧 **نحوه استفاده:**

**1. شناسایی صوتی:**
• هر فایل صوتی را برای من ارسال کنید (MP3, WAV, OGG, M4A, FLAC)
• من آهنگ را شناسایی کرده و اطلاعات دقیق ارائه می‌دهم

**2. حالت اینلاین:**
• در هر چتی، تایپ کنید: @{bot_username} [عبارت جستجو]
• مثال: @{bot_username} Queen Bohemian Rhapsody
• یک نتیجه را انتخاب کنید تا به چت ارسال شود

**3. دستورات جستجو:**
• /track [نام آهنگ] - جستجوی آهنگ خاص
• /artist [نام هنرمند] - جستجوی هنرمند
• /charts - مشاهده چارت‌های جهانی موسیقی
• /top [کشور] - آهنگ‌های برتر در یک کشور

**4. زبان:**
• /language - تغییر زبان ربات (انگلیسی/فارسی)

📝 **نکات:**
• حداکثر حجم فایل: {config['max_file_size_bytes'] // (1024*1024)} مگابایت
• فرمت‌های پشتیبانی شده: MP3, WAV, OGG, M4A, FLAC
• حالت اینلاین در تمام چت‌ها و کانال‌ها کار می‌کند

نیاز به کمک بیشتر دارید؟ با @admin تماس بگیرید"""
}}

# Error messages
ERROR_MESSAGES = {{
    'en': {{
        'audio_recognition_failed': "❌ Sorry, I couldn't identify this audio. Please try with a clearer audio file.",
        'file_too_large': f"❌ File is too large! Maximum size is {config['max_file_size_bytes'] // (1024*1024)}MB.",
        'unsupported_format': "❌ Unsupported file format! Please send MP3, WAV, OGG, M4A, or FLAC files.",
        'no_results': "❌ No results found for your search.",
        'rate_limited': "⚠️ Too many requests! Please wait a moment before trying again.",
        'api_error': "❌ API error occurred. Please try again later."
    }},
    'fa': {{
        'audio_recognition_failed': "❌ متأسفم، نتوانستم این صدا را شناسایی کنم. لطفاً با یک فایل صوتی واضح‌تر دوباره تلاش کنید.",
        'file_too_large': f"❌ فایل خیلی بزرگ است! حداکثر حجم {config['max_file_size_bytes'] // (1024*1024)} مگابایت است.",
        'unsupported_format': "❌ فرمت فایل پشتیبانی نمی‌شود! لطفاً فایل‌های MP3, WAV, OGG, M4A یا FLAC ارسال کنید.",
        'no_results': "❌ نتیجه‌ای برای جستجوی شما یافت نشد.",
        'rate_limited': "⚠️ درخواست‌های زیادی ارسال کرده‌اید! لطفاً لحظه‌ای صبر کرده و دوباره تلاش کنید.",
        'api_error': "❌ خطای API رخ داده است. لطفاً بعداً دوباره تلاش کنید."
    }}
}}
'''
    
    # Backup existing config file if it exists
    if os.path.exists('config.py'):
        backup_name = f'config.py.backup.{__import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")}'
        os.rename('config.py', backup_name)
        print(f"📦 Existing config.py backed up as {backup_name}")
    
    # Write new config file
    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)

def main():
    """Main function"""
    try:
        setup_bot()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()