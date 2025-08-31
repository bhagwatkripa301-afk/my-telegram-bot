import functools
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# Yahan se "." hata diya gaya hai
from config import Config

# Config file se settings load karein
config = Config()

def membership_required(func):
    """
    Ek decorator jo check karta hai ki user ne zaroori channels join kiye hain ya nahi.
    Yeh python-telegram-bot (v13) ke liye banaya gaya hai.
    """
    @functools.wraps(func)
    def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        
        unjoined_channels = []
        for channel in config.REQUIRED_CHANNELS:
            try:
                # v13 mein 'await' nahi hota
                chat_member = context.bot.get_chat_member(chat_id=channel, user_id=user_id)
                if chat_member.status in ['left', 'kicked']:
                    unjoined_channels.append(channel)
            except Exception as e:
                # logger ko config se access karein
                if hasattr(config, 'logger'):
                    config.logger.error(f"Channel {channel} check karte waqt error: {e}")
                unjoined_channels.append(channel)
        
        if not unjoined_channels:
            # Agar sabhi channels join hain, to asli command chalne dein
            return func(update, context, *args, **kwargs)
        else:
            # Agar koi channel join nahi hai, to user ko message bhejein
            keyboard = []
            for channel in unjoined_channels:
                try:
                    chat = context.bot.get_chat(channel)
                    invite_link = chat.invite_link
                    if not invite_link and isinstance(channel, str) and channel.startswith('@'):
                        # Public channels ke liye link banayein
                        invite_link = f"https://t.me/{channel.replace('@', '')}"
                    
                    btn_text = chat.title or str(channel)
                    keyboard.append([InlineKeyboardButton(f"➡️ Join {btn_text}", url=invite_link)])
                except Exception as e:
                    if hasattr(config, 'logger'):
                        config.logger.error(f"Invite link banate waqt error for {channel}: {e}")
                    if isinstance(channel, str):
                        keyboard.append([InlineKeyboardButton(f"➡️ Join {channel}", url=f"https://t.me/{channel.replace('@', '')}")])
            
            update.effective_message.reply_text(
                "⚠️ **Access Denied!**\n\n"
                "Bot ko istemal karne ke liye, aapko pehle yeh sabhi channels join karne honge. Join karne ke baad, apna command dobara try karein.",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown"
            )
            return
            
    return wrapper

