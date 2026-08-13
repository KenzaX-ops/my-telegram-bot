import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask Setup
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Bot Logic
TOKEN = "8611394413:AAHsmSiuC7RRUcCirZzYh01XHeltSsZJjdg"

async def start(update, context):
    args = context.args 
    if args and args[0] == "aboutyou":
        # သင့် Audio ID ကို ဒီမှာ ပြန်စစ်ပြီး ထည့်ပါ
        audio_id = "CQACAgUAAxkBAAEthXZqfeeng9g6FD8Dc2zu6KKqRvKV8wACByAAAntG8FdbAkuPEtnRSD0E" 
        await update.message.reply_audio(audio=audio_id, caption="🎶 About You - The 1975")
    else:
        await update.message.reply_text("မင်္ဂလာပါ! Channel မှ Link ကို နှိပ်၍ သီချင်းရယူနိုင်ပါသည်။")

def main():
    # Flask ကို Background မှာ စတင် Run ပါ
    threading.Thread(target=run_flask).start()
    
    # Bot ကို စတင် Run ပါ
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.run_polling()

if __name__ == "__main__":
    main()

