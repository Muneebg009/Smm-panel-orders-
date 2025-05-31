import logging
import requests
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from datetime import datetime

# 🔐 Your API and BOT Token
API_KEY = '40homc3nz0cptqm2flq9ur95srccggj5ntz4u3o3sqa2fegyk25acx5gkewohbg8'
BOT_TOKEN = '7996856800:AAHZ68hmbZ9y9CvL4Xb5wLpz7VwbFp9337U'

# 🛠 Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 🟢 /start command
def start(update, context):
    update.message.reply_text("👋 Welcome Moeez Bhai!\nUse /order <id> to check order details and time taken.")

# 🔍 /order command
def order(update, context):
    if len(context.args) != 1:
        update.message.reply_text("❌ Use like: /order 244")
        return

    order_id = context.args[0]
    url = f"https://app.smmpanelexpress.com/adminapi/v2/orders/{order_id}"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get("data", {})
    except Exception as e:
        update.message.reply_text("❌ API Error. Try again later.")
        return

    if not data:
        update.message.reply_text("❌ Order not found.")
        return

    # Time calculation
    created_ts = data.get("created_timestamp")
    updated_ts = data.get("last_update_timestamp")
    if created_ts and updated_ts and updated_ts != created_ts:
        diff = datetime.fromtimestamp(updated_ts) - datetime.fromtimestamp(created_ts)
        sec = int(diff.total_seconds())
        h = sec // 3600
        m = (sec % 3600) // 60
        s = sec % 60
        time_taken = f"{h}h {m}m {s}s"
    else:
        time_taken = "⚠️ Not available"

    # 📨 Message
    msg = f"✅ <b>Order Details</b>\n"
    msg += f"🆔 ID: <code>{data.get('id')}</code>\n"
    msg += f"👤 User: <b>{data.get('user')}</b>\n"
    msg += f"📦 Status: <b>{data.get('status')}</b>\n"
    msg += f"📅 Created: <code>{data.get('created')}</code>\n"
    msg += f"📅 Updated: <code>{data.get('last_update')}</code>\n"
    msg += f"🔗 Link: <a href='{data.get('link')}'>Open</a>\n"
    msg += f"⏱️ Time Taken: <b>{time_taken}</b>"

    update.message.reply_text(msg, parse_mode=ParseMode.HTML)

# Main function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("order", order))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()