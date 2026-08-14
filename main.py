import os
import threading
import asyncio
import logging
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask Web Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Token
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    if args and args[0] == "aboutyou":
        audio_id = "CQACAgUAAxkBAAEthXZqfeeng9g6FD8Dc2zu6KKqRvKV8wACByAAAntG8FdbAkuPEtnRSD0E" 
        await update.message.reply_audio(audio=audio_id, caption="🎶 About You - The 1975")
    else:
        await update.message.reply_text("မင်္ဂလာပါ!")

async def main():
    # Flask ကို Thread နဲ့ Run
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Bot ကို အလိုလို ပြန်တက်အောင် Loop လုပ်ပေးခြင်း
    while True:
        try:
            print("Bot is connecting...")
            application = Application.builder().token(TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            
            await application.initialize()
            await application.start()
            await application.updater.start_polling(drop_pending_updates=True)
            
            # Bot အလုပ်လုပ်နေချိန် ရပ်မသွားအောင် စောင့်နေမယ်
            await asyncio.Event().wait()
        except Exception as e:
            print(f"Error occurred: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
