import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask # ဒါလေး အပိုထည့်လိုက်ပါ

# Web Service အတွက် Port အပိုဖွင့်ပေးခြင်း
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

# သင့် Bot Token
TOKEN = "8611394413:AAHsmSiuC7RRUcCirZzYh01XHeltSsZJjdg" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    if args and args[0] == "aboutyou":
        audio_id = "CQACAgUAAxkBAAEthXZqfeeng9g6FD8Dc2zu6KKqRvKV8wACByAAAntG8FdbAkuPEtnRSD0E" 
        await update.message.reply_audio(audio=audio_id, caption="🎶 About You - The 1975")
    else:
        await update.message.reply_text("မင်္ဂလာပါ! Channel မှ Link ကို နှိပ်၍ သီချင်းရယူနိုင်ပါသည်။")

def main():
    # Flask Server ကို Port မှာ စတင် Run ပါ
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
    # Bot ကို Run ပါ
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.run_polling()

if __name__ == "__main__":
    main()

