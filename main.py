import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes

# Flask Web Server (Render Sleeping မဖြစ်အောင်)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# ==================== CONFIGURATION ====================
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE"  # သင့် Bot Token
STORAGE_CHANNEL_ID = -1003905586421  # သီချင်းများ တင်ထားသော Channel ရဲ့ ID
# =======================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    
    # Link ထဲမှာ Post ID နံပါတ် ပါလာခဲ့ရင် (ဥပမာ: /start 15)
    if args and args[0].isdigit():
        msg_id = int(args[0])
        
        try:
            # Messenger လိုမျိုး သီချင်းပို့နေတဲ့ Animation လေး ၃ စက္ကန့် ပြပေးမယ်
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action=ChatAction.UPLOAD_VOICE
            )
            await asyncio.sleep(3) # ၃ စက္ကန့် စောင့်ခိုင်းတာပါ

            # Storage Channel ထဲက Post ID နံပါတ်အတိုင်း သီချင်းဆွဲထုတ်ပြီး Auto ပို့ပေးခြင်း
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id
            )
            return
        except Exception as e:
            await update.message.reply_text("ရှာမတွေ့ပါ သို့မဟုတ် သီချင်းဖိုင် ဖျက်လိုက်ပါပြီ။")
            return

    # ရိုးရိုး /start ပဲ နှိပ်လိုက်ရင် ပေါ်မယ့်စာ
    await update.message.reply_text("မင်္ဂလာပါ! သီချင်းနားထောင်ရန် Channel ထဲက Button ကို နှိပ်ပါခင်ဗျာ။")

async def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Bot Crashed မဖြစ်အောင် အလိုလို ပြန်စပေးမယ့် Loop
    while True:
        try:
            application = Application.builder().token(TOKEN).build()
            application.add_handler(CommandHandler("start", start))
            
            await application.initialize()
            await application.start()
            await application.updater.start_polling(drop_pending_updates=True)
            await asyncio.Event().wait()
        except Exception as e:
            print(f"Error: {e}. Restarting in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
