import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Render Port မပိတ်အောင် Flask Server သုံးခြင်း
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Bot Token
TOKEN = "8611394413:AAHsmSiuC7RRUcCirZzYh01XHeltSsZJjdg" # သင့် Bot Token အမှန် ပြန်ထည့်ပါ

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    if args and args[0] == "aboutyou":
        audio_id = "CQACAgUAAxkBAAEthXZqfeeng9g6FD8Dc2zu6KKqRvKV8wACByAAAntG8FdbAkuPEtnRSD0E" 
        await update.message.reply_audio(audio=audio_id, caption="🎶 About You - The 1975")
    else:
        await update.message.reply_text("မင်္ဂလာပါ! Channel မှ Link ကို နှိပ်၍ သီချင်းရယူနိုင်ပါသည်။")

def main():
    # ၁။ Flask Server ကို သီးသန့် Thread မှာ စတင် Run ပါ
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # ၂။ Telegram Bot ကို စတင် Run ပါ
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    
    print("Bot is starting...")
    bot_app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

