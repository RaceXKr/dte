import os
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, redirect
from threading import Thread
from motor.motor_asyncio import AsyncIOMotorClient

API_ID = int(os.environ.get("API_ID", 29394851))
API_HASH = os.environ.get("API_HASH", "4a97459b3db52a61a35688e9b6b86221")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7859184332:AAFPrkZyrli8RJjaGeX_JClFKiJU4owIg4o")
DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://krkkanish2:kx@cluster0.uhrg1rj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "kdeletebot")

# Database setup
client = AsyncIOMotorClient(DATABASE_URL)
db = client['databas']
groups = db['group_id']

bot = Client(
    "deletebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=300,
    sleep_threshold=10
)

@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
    button = [[
        InlineKeyboardButton("➕ Add me to your Group", url=f"http://t.me/{BOT_USERNAME}?startgroup=none&admin=delete_messages"),
    ], [
        InlineKeyboardButton("📌 Updates Channel", url="https://t.me/botsync"),
    ]]
    await message.reply_text(
        f"**Hello {message.from_user.first_name},\nI am an AutoDelete Bot. I can delete all messages in your group automatically after a certain period of time.\nUsage:** `/set_time <time_in_seconds>`",
        reply_markup=InlineKeyboardMarkup(button),
        parse_mode=enums.ParseMode.MARKDOWN
    )

@bot.on_message(filters.command("set_time"))
async def set_delete_time(_, message):
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply("This command can only be used in groups.")
        return
    
    args = message.text.split()
    if len(args) == 1:
        await message.reply_text("**Please provide the delete time in seconds. Usage:** `/set_time <time_in_seconds>`")
        return
    
    delete_time = args[1]
    if not delete_time.isdigit():
        await message.reply_text("Delete time must be an integer.")
        return
    
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    # Check if the user is an admin
    administrators = [m.user.id async for m in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    if user_id not in administrators:
        await message.reply("Only group admins can enable or disable auto delete.")
        return
    
    # Save to the database
    await groups.update_one(
        {"group_id": chat_id},
        {"$set": {"delete_time": int(delete_time)}},
        upsert=True
    )
    
    await message.reply_text(f"**Set delete time to {delete_time} seconds for this group.**")

@bot.on_message(filters.group & ~filters.command(["set_time", "start"]))
async def delete_message(client, message):
    chat_id = message.chat.id
    group = await groups.find_one({"group_id": chat_id})
    if not group:
        return
    
    delete_time = int(group.get("delete_time", 0))
    if delete_time > 0:
        await asyncio.sleep(delete_time)
        try:
            await client.delete_messages(chat_id, message.id)  # Corrected attribute
        except Exception as e:
            print(f"An error occurred: {e}\nGroup ID: {chat_id}")

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
    bot.run()

# Keep-alive function using aiohttp
import asyncio
from aiohttp import ClientSession

async def keep_alive():
    url = f"https://{os.environ.get('APP_NAME', 'your-app-name')}.koyeb.app"
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    print(f"Keep-alive ping sent! Status: {response.status}")
        except Exception as e:
            print(f"Keep-alive error: {e}")
        await asyncio.sleep(300)

asyncio.create_task(keep_alive())
