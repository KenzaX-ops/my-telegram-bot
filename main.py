import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== CONFIGURATION ====================
TOKEN = "8809216809:AAFOcO0RmmEQbeQ2NuYtfYfXZv2DSL7LToE"
STORAGE_CHANNEL_ID = -1003905586421

# စမ်းသပ်ရန်အတွက် ၁၀ စက္ကန့်ထားပေးထားပါသည်
AUTO_DELETE_AUDIO_SECONDS = 10  
# =======================================================

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Live and Running!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

# မက်ဆေ့ခ်ျကို အချိန်စေ့ရင် အလိုအလျောက် ဖျက်ပေးမယ့် Async Function
async def delete_message_after_delay(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"Deleted message {message_id} from chat {chat_id}")
    except Exception as e:
        print(f"Failed to delete message: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args 
    chat_id = update.effective_chat.id
    
    # Link ထဲမှာ /start 10 ဆိုပြီး ပါလာခဲ့ရင်
    if args and args[0].isdigit():
        msg_id = int(args[0])
        try:
            # ၁။ "Sending audio, please wait..." ဆိုတဲ့ စာတိုလေး ပထမဆုံး ပို့မယ်
            temp_msg = await update.message.reply_text("🎵 Sending audio, please wait...")

            # ၃ စက္ကန့် အသံပို့နေသလို စောင့်ခိုင်းမယ်
            await context.bot.send_chat_action(
                chat_id=chat_id, 
                action=ChatAction.UPLOAD_VOICE
            )
            await asyncio.sleep(3)

            # ၂။ ခဏစောင့်ခိုင်းတဲ့ စာတိုလေးကို Auto ဖျက်လိုက်မယ်
            try:
                await temp_msg.delete()
            except Exception:
                pass

            # ၃။ Storage Channel ထဲက သီချင်း ပို့ပေးမယ်
            audio_msg = await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id
            )

            # ၄။ သီချင်းကို ၁၀ စက္ကန့်ပြည့်ရင် Auto Delete ပြန်လုပ်မည်
            asyncio.create_task(
                delete_message_after_delay(
                    context, 
                    chat_id, 
                    audio_msg.message_id, 
                    AUTO_DELETE_AUDIO_SECONDS
                )
            )
            return

        except Exception as e:
            print(f"Error sending audio: {e}")
            await update.message.reply_text("⚠️ ရှာမတွေ့ပါ သို့မဟုတ် Storage Channel ထဲတွင် Bot ကို Admin ထည့်မထားပါ။")
            return

    await update.message.reply_text("မင်္ဂလာပါ! သီချင်းနားထောင်ရန် Channel ထဲက Button ကို နှိပ်ပါခင်ဗျာ။")

def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("Flask Web Server Started Background...")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print(">>> Telegram Bot is ACTIVE and RUNNING! <<<")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
