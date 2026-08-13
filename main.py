import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask Web Server setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive and Running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Token
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE" # သင့် Bot Token အမှန် ထည့်ပေးပါ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    if args and args[0] == "aboutyou":
        # သီချင်းပို့ပေးမည့် Audio File ID
        audio_id = "CQACAgUAAxkBAAEthXZqfeeng9g6FD8Dc2zu6KKqRvKV8wACByAAAntG8FdbAkuPEtnRSD0E" 
        await update.message.reply_audio(audio=audio_id, caption="🎶 About You - The 1975")
    else:
        await update.message.reply_text("မင်္ဂလာပါ! Channel မှ Link ကို နှိပ်၍ သီချင်းရယူနိုင်ပါသည်။")

async def main():
    # Flask ကို Background Thread မှာ Run မည်
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Telegram Bot ကို Init လုပ်မည်
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # Bot ကို စတင် Run မည်
    async with application:
        await application.start()
        await application.updater.start_polling(drop_pending_updates=True)
        print("Bot started successfully!")
        # Server ပိတ်မသွားအောင် ထိန်းထားမည်
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass

