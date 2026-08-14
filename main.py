import os
import asyncio
import threading
from flask import Flask
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, InlineQueryHandler

# ==================== CONFIGURATION ====================
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE"
STORAGE_CHANNEL_ID = -1003905586421
AUTO_DELETE_AUDIO_SECONDS = 10 
# =======================================================

# Database (Simple Memory Storage)
user_stats = {}
current_lang = 'my' # Default Language

# Language Dictionary
LANGS = {
    'my': {
        'welcome': "မင်္ဂလာပါ! ကျွန်တော်က သီချင်း Bot ပါ။ Channel ထဲက Button တွေကနေတစ်ဆင့် သီချင်းတွေ နားထောင်နိုင်ပါတယ်။",
        'stats': "📊 သင်နားထောင်ပြီးသော သီချင်းအရေအတွက် - {count} ပုဒ်",
        'lang_changed': "ဘာသာစကားကို မြန်မာလိုသို့ ပြောင်းလိုက်ပါပြီ။"
    },
    'en': {
        'welcome': "Welcome! I am your music bot. You can listen to songs via channel buttons.",
        'stats': "📊 Songs you have listened to - {count}",
        'lang_changed': "Language changed to English."
    }
}

# Song Database (Inline Search အတွက်)
SONG_DATABASE = [
    {"id": "1", "title": "သီချင်း ၁"},
    {"id": "2", "title": "သီချင်း ၂"},
]

app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Live and Running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

async def delete_message_after_delay(context, chat_id, message_id, delay):
    await asyncio.sleep(delay)
    try: await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    except: pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args 
    
    if args and args[0].isdigit():
        msg_id = int(args[0])
        # Stats +1
        user_stats[user_id] = user_stats.get(user_id, 0) + 1
        
        try:
            temp_msg = await update.message.reply_text("🎵 Sending audio...")
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_VOICE)
            await asyncio.sleep(3)
            try: await temp_msg.delete()
            except: pass
            
            audio_msg = await context.bot.copy_message(chat_id=update.effective_chat.id, from_chat_id=STORAGE_CHANNEL_ID, message_id=msg_id)
            asyncio.create_task(delete_message_after_delay(context, update.effective_chat.id, audio_msg.message_id, AUTO_DELETE_AUDIO_SECONDS))
            return
        except: await update.message.reply_text("⚠️ Error!")
    else:
        await update.message.reply_text(LANGS[current_lang]['welcome'])

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    count = user_stats.get(update.effective_user.id, 0)
    await update.message.reply_text(LANGS[current_lang]['stats'].format(count=count))

async def toggle_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_lang
    current_lang = 'en' if current_lang == 'my' else 'my'
    await update.message.reply_text(LANGS[current_lang]['lang_changed'])

async def inline_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query: return
    results = [
        InlineQueryResultArticle(
            id=s['id'], title=s['title'],
            input_message_content=InputTextMessageContent(f"/start {s['id']}")
        ) for s in SONG_DATABASE if query.lower() in s['title'].lower()
    ]
    await update.inline_query.answer(results)

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("lang", toggle_lang))
    application.add_handler(InlineQueryHandler(inline_search))
    
    print(">>> Telegram Bot is ACTIVE and RUNNING! <<<")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

