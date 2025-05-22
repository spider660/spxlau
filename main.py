from pyrogram import Client 
import json
import asyncio
from FUNC.server_stats import *
from FUNC.scraperfunc import channel_cleanup_background

plugins = dict(root="BOT")

with open("FILES/config.json", "r", encoding="utf-8") as f:
    DATA      = json.load(f)
    API_ID    = DATA["API_ID"]
    API_HASH  = DATA["API_HASH"]
    BOT_TOKEN = DATA["BOT_TOKEN"]

user = Client( 
            "Scrapper", 
             api_id   = API_ID, 
             api_hash = API_HASH
              )

bot = Client(
    "MY_BOT", 
    api_id    = API_ID, 
    api_hash  = API_HASH, 
    bot_token = BOT_TOKEN, 
    plugins   = plugins 
)



async def start_background_tasks():
    """Start background tasks for channel cleanup"""
    asyncio.create_task(channel_cleanup_background())
    print("Background channel cleanup task started")

if __name__ == "__main__":
    # send_server_alert()
    print("SPILUXX BOT IS ACTIVE✅")
    print("NOW START YOUR BOT ")
    
    # Start background tasks
    loop = asyncio.get_event_loop()
    loop.create_task(start_background_tasks())
    
    # Run the bot
    bot.run()
