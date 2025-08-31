#!/usr/bin/env python3
"""
Enhanced Telegram Bot for Course Link Finding
Main entry point for the application
"""

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
# keep_alive ki zaroorat nahi hai kyunki Render alag tarike se kaam karta hai

from bot.config import Config
from bot.handlers import (
    start_handler, help_handler, search_handler, callback_handler,
    settings_handler, history_handler, favorites_handler
)
from bot.database import Database

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def error_handler(update, context):
    """Log errors"""
    # Naye version (v20+) mein `update` object None ho sakta hai
    if update:
        logger.warning(f'Update "{update}" caused error "{context.error}"')

def main():
    """Main function to start the bot"""
    # Initialize configuration
    config = Config()
    
    # Initialize database
    db = Database()
    
    # v13 ke liye Updater ka istemal karein
    updater = Updater(config.BOT_TOKEN, use_context=True)
    
    # Dispatcher se handlers register karein
    dp = updater.dispatcher
    
    # Handlers jodein
    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("help", help_handler))
    dp.add_handler(CommandHandler("settings", settings_handler))
    dp.add_handler(CommandHandler("history", history_handler))
    dp.add_handler(CommandHandler("favorites", favorites_handler))
    
    # Message handlers (Filters.text & ~Filters.command v13 ke liye)
    dp.add_handler(MessageHandler(
        Filters.text & ~Filters.command, 
        search_handler
    ))
    
    # Callback query handler
    dp.add_handler(CallbackQueryHandler(callback_handler))
    
    # Error handler
    dp.add_error_handler(error_handler)
    
    # Bot start karein
    logger.info("🚀 Enhanced Course Bot is starting...")
    print("🤖 Bot is running... Press Ctrl+C to stop")
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()


