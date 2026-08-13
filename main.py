from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# သင့် Bot Token
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE" 

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    if args:
        file_key = args[0] 
        
        if file_key == "aboutyou":
            # ခုနက ရလာတဲ့ Audio File ID ကို ဒီမှာ ကွက်တိ ထည့်လိုက်ပါပြီ
            audio_id = "CQACAgUAAxkBAAEthXZqfeeng9g6FD8Dc2zu6KKqRvKV8wACByAAAntG8FdbAkuPEtnRSD0E" 
            await update.message.reply_audio(audio=audio_id, caption="🎶 About You - The 1975")
            
    else:
        await update.message.reply_text("မင်္ဂလာပါ! Channel မှ Link ကို နှိပ်၍ သီချင်းရယူနိုင်ပါသည်။")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("🤖 Render Bot Server is Running 24/7...")
    app.run_polling()

if __name__ == "__main__":
    main()

