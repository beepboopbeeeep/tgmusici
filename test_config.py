#!/usr/bin/env python3
"""
Test script to verify ShazamIO Telegram Bot configuration
"""

import sys
import os
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

def test_config():
    """Test the configuration file"""
    print("🔍 Testing ShazamIO Telegram Bot Configuration")
    print("=" * 50)
    
    try:
        # Import configuration
        import config
        
        print("✅ Configuration file loaded successfully")
        
        # Check required settings
        required_settings = [
            'TELEGRAM_BOT_TOKEN',
            'BOT_USERNAME',
            'DEFAULT_LANGUAGE'
        ]
        
        missing_settings = []
        for setting in required_settings:
            if not hasattr(config, setting):
                missing_settings.append(setting)
        
        if missing_settings:
            print(f"❌ Missing required settings: {', '.join(missing_settings)}")
            return False
        
        # Check bot token format
        if config.TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
            print("❌ Bot token not configured. Please run: python setup.py")
            return False
        
        if len(config.TELEGRAM_BOT_TOKEN) < 30:
            print("❌ Bot token appears to be invalid (too short)")
            return False
        
        print("✅ Bot token configured")
        print(f"✅ Bot username: @{config.BOT_USERNAME}")
        print(f"✅ Default language: {config.DEFAULT_LANGUAGE}")
        
        # Check feature flags
        features = [
            ('Audio Recognition', config.ENABLE_AUDIO_RECOGNITION),
            ('Inline Mode', config.ENABLE_INLINE_MODE),
            ('Language Selection', config.ENABLE_LANGUAGE_SELECTION),
            ('Track Info', config.ENABLE_TRACK_INFO),
            ('Artist Info', config.ENABLE_ARTIST_INFO),
            ('Music Charts', config.ENABLE_CHARTS),
            ('Rate Limiting', config.ENABLE_RATE_LIMITING),
        ]
        
        print("\n🔧 Enabled Features:")
        for name, enabled in features:
            status = "✅" if enabled else "❌"
            print(f"  {status} {name}")
        
        # Check rate limiting settings
        if config.ENABLE_RATE_LIMITING:
            print(f"\n⚡ Rate Limiting: {config.MAX_REQUESTS_PER_MINUTE} requests per minute")
            print(f"📁 Max file size: {config.MAX_AUDIO_FILE_SIZE // (1024*1024)}MB")
        
        # Check admin settings
        if config.ADMIN_USER_IDS:
            print(f"\n👤 Admin users: {len(config.ADMIN_USER_IDS)} configured")
        
        print("\n✅ All configuration checks passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import configuration: {e}")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing Dependencies")
    print("=" * 30)
    
    required_packages = [
        ('python-telegram-bot', 'telegram'),
        ('shazamio', 'shazamio'),
        ('aiohttp', 'aiohttp'),
    ]
    
    missing_packages = []
    
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} (missing)")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True

def main():
    """Main test function"""
    print("🎵 ShazamIO Telegram Bot - Configuration Test")
    print("=" * 60)
    
    config_ok = test_config()
    deps_ok = test_dependencies()
    
    print("\n" + "=" * 60)
    
    if config_ok and deps_ok:
        print("🎉 Configuration test PASSED!")
        print("\n🚀 Next steps:")
        print("1. Enable inline mode in @BotFather")
        print("2. Run the bot: python bot.py")
        print("3. Test with /start command")
        print("4. Try sending an audio file")
        return 0
    else:
        print("❌ Configuration test FAILED!")
        print("\n🔧 Fix the issues above and try again")
        return 1

if __name__ == "__main__":
    sys.exit(main())