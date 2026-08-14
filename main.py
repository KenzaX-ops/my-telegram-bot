import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== CONFIGURATION (အဆင်သင့် ထည့်ပေးထားသည်) ====================
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE"
STORAGE_CHANNEL_ID = -1003905586421
# ==============================================================================

# Flask Web Server (Render မအိပ်အောင် နိုးထားပေးရန်)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live and Running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    
    # Link ထဲမှာ /start 10 ဆိုပြီး ပါလာခဲ့ရင်
    if args and args[0].isdigit():
        msg_id = int(args[0])
        try:
            # Messenger လိုမျိုး Typing/Sending audio ၃ စက္ကန့် ပြပေးမယ်
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, 
                action=ChatAction.UPLOAD_VOICE
            )
            await asyncio.sleep(3) # ၃ စက္ကန့် စောင့်ခိုင်းခြင်း

            # Storage Channel ထဲက Post ID နံပါတ်အတိုင်း သီချင်း Auto ပို့ပေးခြင်း
            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id
            )
            return
        except Exception as e:
            print(f"Error sending audio: {e}")
            await update.message.reply_text("ရှာမတွေ့ပါ သို့မဟုတ် Storage Channel ထဲတွင် Bot ကို Admin ထည့်မထားပါ။")
            return

    # ရိုးရိုး /start နှိပ်ရင် ပေါ်မယ့်စာ
    await update.message.reply_text("မင်္ဂလာပါ! သီချင်းနားထောင်ရန် Channel ထဲက Button ကို နှိပ်ပါခင်ဗျာ။")

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Telegram Bot Started Polling...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    # Web Server ကို နောက်ကွယ် (Thread) မှာ Run မယ်
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Telegram Bot ကို Main Thread မှာ Run မယ်
    run_bot()
