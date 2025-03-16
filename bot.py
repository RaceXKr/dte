import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, redirect
from threading import Thread
from motor.motor_asyncio import AsyncIOMotorClient

API_ID = int(os.environ.get("API_ID", 29394851))
API_HASH = os.environ.get("API_HASH", "4a97459b3db52a61a35688e9b6b86221")
USER_SESSION = os.environ.get("USER_SESSION", "AgHAh6MAtgaeUygtEKQ79xLpyRtnQtKiEOTvpRajN6EFDRG6m8cmj_qAdmyBFC7ikQkZaprRhNcUcY5WtJaAHFQQxA0rcSP5XBfAWVfpXQBWRAgRX8OtljxeW9NPaVLj5us2t2jPW1MGem7ozdedoTqSDuItwvtnGDt2EilVC1QFyuq-nCRHA_3Auu1FY0pspnD9jZBHXw-s8OaERD_m5qwDv1R6avKuiiE2uMktXFtoYKa9qTOfe82VnvMyF95HA9_m_TBfmNL-exkWjTQFVV1G9xD2TasjfKm8S0YsJphWPR8oO73ErjDleU5HrZMJ-NCwubGn8ZFWUnRPRk3JGTtShpeEDgAAAAGdPH8SAA")  # Use a Pyrogram user session
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://krkkanish2:kx@cluster0.uhrg1rj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "kdeletebot")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002429133029"))  # Log channel ID

# Database setup
client = AsyncIOMotorClient(DATABASE_URL)
db = client['databas']
groups = db['group_id']

user_bot = Client("user_deletebot", session_string=USER_SESSION, api_id=API_ID, api_hash=API_HASH)

@user_bot.on_message(filters.command("accept_all"))
async def accept_all_requests(client, message):
    chat_id = message.chat.id
    approved_count = 0
    async for request in user_bot.get_chat_join_requests(chat_id):
        try:
            await user_bot.approve_chat_join_request(chat_id, request.from_user.id)
            approved_count += 1
        except Exception as e:
            print(f"Error approving {request.from_user.id}: {e}")
    
    await message.reply(f"✅ Approved {approved_count} pending requests!")
    await user_bot.send_message(LOG_CHANNEL, f"Approved {approved_count} requests in {message.chat.title} ({chat_id})")

# Flask configuration
app = Flask(__name__)

@app.route('/')
def index():
    return redirect("https://telegram.me/AboutRazi", code=302)

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    user_bot.run()

# Keep-alive function using aiohttp
import asyncio
from aiohttp import ClientSession

async def keep_alive():
    url = f"https://low-lesly-selvarajsangeeth419-4a099a4d.koyeb.app/"
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    print(f"Keep-alive ping sent! Status: {response.status}")
        except Exception as e:
            print(f"Keep-alive error: {e}")
        await asyncio.sleep(300)

asyncio.create_task(keep_alive())
