#!/usr/bin/env python3
"""
ShazamIO Telegram Bot
A powerful music identification and search bot for Telegram
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from io import BytesIO

from telegram import (
    Update,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Audio,
    Voice,
    Document,
    BotCommand,
    BotCommandScopeDefault,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
from telegram.error import TelegramError

from shazamio import Shazam, Serialize
import json

# Import configuration
from config import *

# Set up logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE) if LOG_FILE else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Rate limiting storage
user_requests: Dict[int, List[datetime]] = {}

class ShazamIOBot:
    def __init__(self):
        self.shazam = Shazam()
        self.user_languages: Dict[int, str] = {}
        self.user_data: Dict[int, Dict] = {}
        
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language or default"""
        return self.user_languages.get(user_id, DEFAULT_LANGUAGE)
    
    def set_user_language(self, user_id: int, language: str):
        """Set user's preferred language"""
        self.user_languages[user_id] = language
    
    def get_text(self, user_id: int, text_dict: Dict) -> str:
        """Get text in user's preferred language"""
        lang = self.get_user_language(user_id)
        return text_dict.get(lang, text_dict.get('en', ''))
    
    def get_error_text(self, user_id: int, error_key: str) -> str:
        """Get error message in user's preferred language"""
        lang = self.get_user_language(user_id)
        return ERROR_MESSAGES[lang].get(error_key, ERROR_MESSAGES['en'].get(error_key, ''))
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Check if user is rate limited"""
        if not ENABLE_RATE_LIMITING:
            return True
            
        now = datetime.now()
        if user_id not in user_requests:
            user_requests[user_id] = []
        
        # Clean old requests (older than 1 minute)
        user_requests[user_id] = [
            req_time for req_time in user_requests[user_id]
            if now - req_time < timedelta(minutes=1)
        ]
        
        # Check if user exceeded limit
        if len(user_requests[user_id]) >= MAX_REQUESTS_PER_MINUTE:
            return False
        
        user_requests[user_id].append(now)
        return True
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        message = self.get_text(user_id, START_MESSAGE).format(
            bot_username=BOT_USERNAME
        )
        
        # Create language selection keyboard
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        message = self.get_text(user_id, HELP_MESSAGE).format(
            bot_username=BOT_USERNAME
        )
        
        await update.message.reply_text(
            message,
            parse_mode='Markdown'
        )
    
    async def about_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /about command"""
        user_id = update.effective_user.id
        message = self.get_text(user_id, BOT_ABOUT_TEXT)
        
        await update.message.reply_text(message)
    
    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command"""
        keyboard = [
            [
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
                InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        user_id = update.effective_user.id
        current_lang = self.get_user_language(user_id)
        current_lang_text = "English" if current_lang == 'en' else "فارسی"
        
        message = f"🌐 Current language: {current_lang_text}\n\nPlease select your preferred language:"
        
        await update.message.reply_text(message, reply_markup=reply_markup)
    
    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection callback"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        lang_code = query.data.replace('lang_', '')
        
        self.set_user_language(user_id, lang_code)
        
        lang_text = "English" if lang_code == 'en' else "فارسی"
        message = f"✅ Language changed to {lang_text}"
        
        await query.edit_message_text(message)
    
    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle audio file recognition"""
        if not ENABLE_AUDIO_RECOGNITION:
            return
            
        user_id = update.effective_user.id
        
        if not self.check_rate_limit(user_id):
            error_msg = self.get_error_text(user_id, 'rate_limited')
            await update.message.reply_text(error_msg)
            return
        
        # Check if message has audio
        audio = None
        if update.message.audio:
            audio = update.message.audio
        elif update.message.voice:
            audio = update.message.voice
        elif update.message.document and any(
            update.message.document.file_name.lower().endswith(ext)
            for ext in SUPPORTED_AUDIO_FORMATS
        ):
            audio = update.message.document
        
        if not audio:
            error_msg = self.get_error_text(user_id, 'unsupported_format')
            await update.message.reply_text(error_msg)
            return
        
        # Check file size
        if audio.file_size > MAX_AUDIO_FILE_SIZE:
            error_msg = self.get_error_text(user_id, 'file_too_large')
            await update.message.reply_text(error_msg)
            return
        
        # Send processing message
        processing_msg = await update.message.reply_text("🎵 Processing audio file...")
        
        try:
            # Download audio file
            file = await context.bot.get_file(audio.file_id)
            audio_data = await file.download_as_bytearray()
            
            # Save to temporary file
            temp_file = f"temp_{user_id}_{audio.file_id}.mp3"
            with open(temp_file, 'wb') as f:
                f.write(audio_data)
            
            # Recognize song
            result = await self.shazam.recognize(temp_file)
            
            # Clean up temp file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            if result and result.get('track'):
                track = result['track']
                await self.send_track_info(update, track, user_id)
            else:
                error_msg = self.get_error_text(user_id, 'audio_recognition_failed')
                await update.message.reply_text(error_msg)
            
            # Delete processing message
            await processing_msg.delete()
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            error_msg = self.get_error_text(user_id, 'api_error')
            await update.message.reply_text(error_msg)
            await processing_msg.delete()
    
    async def send_track_info(self, update: Update, track_data: Dict, user_id: int):
        """Send track information to user"""
        try:
            serialized = Serialize.track(track_data)
            
            # Create message
            title = serialized.title or "Unknown Title"
            artist = serialized.subtitle or "Unknown Artist"
            album = serialized.sections.get('metadata', [{}])[0].get('text', 'Unknown Album') if serialized.sections else 'Unknown Album'
            
            message = f"🎵 **{title}**\n"
            message += f"👤 **Artist:** {artist}\n"
            message += f"💿 **Album:** {album}\n"
            
            # Add genres if available
            if hasattr(serialized, 'genres') and serialized.genres:
                message += f"🎼 **Genre:** {', '.join(serialized.genres)}\n"
            
            # Add year if available
            if hasattr(serialized, 'year') and serialized.year:
                message += f"📅 **Year:** {serialized.year}\n"
            
            # Add Spotify link if available
            if hasattr(serialized, 'spotify_url') and serialized.spotify_url:
                message += f"🎧 [Listen on Spotify]({serialized.spotify_url})\n"
            
            # Add Apple Music link if available
            if hasattr(serialized, 'apple_music_url') and serialized.apple_music_url:
                message += f"🍎 [Listen on Apple Music]({serialized.apple_music_url})\n"
            
            # Add YouTube link if available
            if hasattr(serialized, 'youtube_url') and serialized.youtube_url:
                message += f"📺 [Watch on YouTube]({serialized.youtube_url})\n"
            
            # Create keyboard with action buttons
            keyboard = []
            row = []
            
            if hasattr(serialized, 'spotify_url') and serialized.spotify_url:
                row.append(InlineKeyboardButton("🎧 Spotify", url=serialized.spotify_url))
            
            if hasattr(serialized, 'apple_music_url') and serialized.apple_music_url:
                row.append(InlineKeyboardButton("🍎 Apple Music", url=serialized.apple_music_url))
            
            if row:
                keyboard.append(row)
            
            # Add similar songs button
            keyboard.append([InlineKeyboardButton("🎵 Similar Songs", callback_data=f"similar_{track_data.get('key', '')}")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Add album art if available
            if hasattr(serialized, 'images') and serialized.images:
                # Get the largest image
                image_url = max(serialized.images, key=lambda x: x.get('width', 0)).get('url', '')
                if image_url:
                    await update.message.reply_photo(
                        photo=image_url,
                        caption=message,
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
                else:
                    await update.message.reply_text(
                        message,
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
            else:
                await update.message.reply_text(
                    message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Error sending track info: {e}")
            error_msg = self.get_error_text(user_id, 'api_error')
            await update.message.reply_text(error_msg)
    
    async def inline_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline queries"""
        if not ENABLE_INLINE_MODE:
            return
            
        query = update.inline_query
        if not query.query:
            return
        
        user_id = query.from_user.id
        
        if not self.check_rate_limit(user_id):
            return
        
        try:
            # Search for tracks
            results = await self.shazam.search_track(query=query.query, limit=MAX_INLINE_RESULTS)
            
            if not results or not results.get('tracks', {}).get('hits'):
                return
            
            inline_results = []
            
            for hit in results['tracks']['hits'][:MAX_INLINE_RESULTS]:
                track = hit.get('track', {})
                if not track:
                    continue
                
                try:
                    serialized = Serialize.track(track)
                    
                    title = serialized.title or "Unknown Title"
                    artist = serialized.subtitle or "Unknown Artist"
                    
                    # Create message content
                    message_text = f"🎵 **{title}**\n👤 {artist}"
                    
                    if hasattr(serialized, 'spotify_url') and serialized.spotify_url:
                        message_text += f"\n🎧 [Listen on Spotify]({serialized.spotify_url})"
                    
                    # Create inline result
                    result = InlineQueryResultArticle(
                        id=str(track.get('key', '')),
                        title=f"{title} - {artist}",
                        description=f"Track by {artist}",
                        input_message_content=InputTextMessageContent(
                            message_text=message_text,
                            parse_mode='Markdown'
                        ),
                        thumb_url=serialized.images[0].get('url', '') if serialized.images else '',
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("🎧 Spotify", url=serialized.spotify_url)] if hasattr(serialized, 'spotify_url') and serialized.spotify_url else [],
                            [InlineKeyboardButton("🍎 Apple Music", url=serialized.apple_music_url)] if hasattr(serialized, 'apple_music_url') and serialized.apple_music_url else []
                        ])
                    )
                    
                    inline_results.append(result)
                    
                except Exception as e:
                    logger.error(f"Error processing inline result: {e}")
                    continue
            
            if inline_results:
                await query.answer(inline_results, cache_time=300)
                
        except Exception as e:
            logger.error(f"Error in inline query: {e}")
    
    async def track_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /track command"""
        if not ENABLE_TRACK_INFO:
            return
            
        if not context.args:
            await update.message.reply_text("Please provide a track name. Usage: /track [song name]")
            return
        
        user_id = update.effective_user.id
        
        if not self.check_rate_limit(user_id):
            error_msg = self.get_error_text(user_id, 'rate_limited')
            await update.message.reply_text(error_msg)
            return
        
        query = ' '.join(context.args)
        
        try:
            results = await self.shazam.search_track(query=query, limit=1)
            
            if results and results.get('tracks', {}).get('hits'):
                track = results['tracks']['hits'][0].get('track', {})
                if track:
                    await self.send_track_info(update, track, user_id)
                else:
                    error_msg = self.get_error_text(user_id, 'no_results')
                    await update.message.reply_text(error_msg)
            else:
                error_msg = self.get_error_text(user_id, 'no_results')
                await update.message.reply_text(error_msg)
                
        except Exception as e:
            logger.error(f"Error in track command: {e}")
            error_msg = self.get_error_text(user_id, 'api_error')
            await update.message.reply_text(error_msg)
    
    async def artist_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /artist command"""
        if not ENABLE_ARTIST_INFO:
            return
            
        if not context.args:
            await update.message.reply_text("Please provide an artist name. Usage: /artist [artist name]")
            return
        
        user_id = update.effective_user.id
        
        if not self.check_rate_limit(user_id):
            error_msg = self.get_error_text(user_id, 'rate_limited')
            await update.message.reply_text(error_msg)
            return
        
        query = ' '.join(context.args)
        
        try:
            results = await self.shazam.search_artist(query=query, limit=1)
            
            if results and results.get('artists', {}).get('hits'):
                artist_data = results['artists']['hits'][0]
                artist_id = artist_data.get('artist', {}).get('id')
                
                if artist_id:
                    artist_info = await self.shazam.artist_about(artist_id)
                    serialized = Serialize.artist(artist_info)
                    
                    message = f"👤 **{serialized.name or 'Unknown Artist'}**\n"
                    
                    if hasattr(serialized, 'genres') and serialized.genres:
                        message += f"🎼 **Genres:** {', '.join(serialized.genres)}\n"
                    
                    if hasattr(serialized, 'verified') and serialized.verified:
                        message += "✅ **Verified Artist**\n"
                    
                    if hasattr(serialized, 'followers') and serialized.followers:
                        message += f"👥 **Followers:** {serialized.followers:,}\n"
                    
                    await update.message.reply_text(message, parse_mode='Markdown')
                else:
                    error_msg = self.get_error_text(user_id, 'no_results')
                    await update.message.reply_text(error_msg)
            else:
                error_msg = self.get_error_text(user_id, 'no_results')
                await update.message.reply_text(error_msg)
                
        except Exception as e:
            logger.error(f"Error in artist command: {e}")
            error_msg = self.get_error_text(user_id, 'api_error')
            await update.message.reply_text(error_msg)
    
    async def charts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /charts command"""
        if not ENABLE_CHARTS:
            return
            
        user_id = update.effective_user.id
        
        if not self.check_rate_limit(user_id):
            error_msg = self.get_error_text(user_id, 'rate_limited')
            await update.message.reply_text(error_msg)
            return
        
        try:
            # Get world top tracks
            results = await self.shazam.top_world_tracks(limit=10)
            
            if results and results.get('tracks'):
                message = "🌍 **Top 10 Global Tracks**\n\n"
                
                for i, track in enumerate(results['tracks'][:10], 1):
                    try:
                        serialized = Serialize.track(track)
                        title = serialized.title or "Unknown Title"
                        artist = serialized.subtitle or "Unknown Artist"
                        message += f"{i}. **{title}** - {artist}\n"
                    except Exception as e:
                        logger.error(f"Error serializing track: {e}")
                        continue
                
                await update.message.reply_text(message, parse_mode='Markdown')
            else:
                error_msg = self.get_error_text(user_id, 'no_results')
                await update.message.reply_text(error_msg)
                
        except Exception as e:
            logger.error(f"Error in charts command: {e}")
            error_msg = self.get_error_text(user_id, 'api_error')
            await update.message.reply_text(error_msg)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            user_id = update.effective_user.id
            error_msg = self.get_error_text(user_id, 'api_error')
            try:
                await update.effective_message.reply_text(error_msg)
            except Exception:
                pass
    
    def setup_handlers(self, application: Application):
        """Set up all handlers"""
        # Command handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("about", self.about_command))
        application.add_handler(CommandHandler("language", self.language_command))
        
        if ENABLE_TRACK_INFO:
            application.add_handler(CommandHandler("track", self.track_command))
        
        if ENABLE_ARTIST_INFO:
            application.add_handler(CommandHandler("artist", self.artist_command))
        
        if ENABLE_CHARTS:
            application.add_handler(CommandHandler("charts", self.charts_command))
        
        # Callback handler for language selection
        if ENABLE_LANGUAGE_SELECTION:
            application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        
        # Inline query handler
        if ENABLE_INLINE_MODE:
            application.add_handler(InlineQueryHandler(self.inline_query))
        
        # Audio message handler
        if ENABLE_AUDIO_RECOGNITION:
            application.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.Document.ALL, self.handle_audio))
        
        # Error handler
        application.add_error_handler(self.error_handler)
    
    async def set_bot_commands(self, application: Application):
        """Set bot commands"""
        commands = [
            BotCommand("start", "Start the bot and see welcome message"),
            BotCommand("help", "Show help information"),
            BotCommand("about", "About this bot"),
            BotCommand("language", "Change bot language"),
        ]
        
        if ENABLE_TRACK_INFO:
            commands.append(BotCommand("track", "Search for a track"))
        
        if ENABLE_ARTIST_INFO:
            commands.append(BotCommand("artist", "Search for an artist"))
        
        if ENABLE_CHARTS:
            commands.append(BotCommand("charts", "View global music charts"))
        
        await application.bot.set_my_commands(commands, scope=BotCommandScopeDefault())
    
    async def run(self):
        """Run the bot"""
        try:
            # Create application
            application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
            
            # Set up handlers
            self.setup_handlers(application)
            
            # Set bot commands
            await self.set_bot_commands(application)
            
            logger.info("Bot started successfully!")
            
            # Start polling
            await application.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise

def main():
    """Main function"""
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ Error: Please set your Telegram bot token in config.py")
        print("Get your token from @BotFather on Telegram")
        return
    
    bot = ShazamIOBot()
    
    # Run the bot
    asyncio.run(bot.run())

if __name__ == "__main__":
    main()