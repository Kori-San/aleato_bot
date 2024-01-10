from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
from telethon.tl.custom.message import Message

from src.forum.random_topics import get_all_topics, random_topics

import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the environment variables
API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN not found in .env file")

API_ID = os.getenv("API_ID")
if not API_ID:
    raise ValueError("API_ID not found in .env file")

API_HASH = os.getenv("API_HASH")
if not API_HASH:
    raise ValueError("API_HASH not found in .env file")

USER_SESSION = os.getenv("USER_SESSION")
if not USER_SESSION:
    raise ValueError("USER_SESSION not found in .env file")

BOT_SESSION = os.getenv("BOT_SESSION")
if not BOT_SESSION:
    raise ValueError("BOT_SESSION not found in .env file")

bot_client = TelegramClient(BOT_SESSION, API_ID, API_HASH).start(bot_token=API_TOKEN)

@bot_client.on(events.NewMessage(pattern='/randomtopics'))  # Command to trigger the bot
async def random_topics_command(event: Message) -> None:
    try:
        # Get the ID of the chat that called the bot
        chat_id = event.chat_id
        peer_id = event.message.peer_id.channel_id 
        
        topics = await get_all_topics(chat_id, USER_SESSION, API_ID, API_HASH)

        random_count = 5
        randoms = random_topics(random_count, topics)

        # Send a message with the link to the forum topic
        response_string = ""
        for i, topic in enumerate(randoms, start = 1):
            response_string += f"{i}. {topic.title}\n    -> t.me/c/{peer_id}/{topic.id}\n"
        
        await event.reply(response_string)
    except Exception as e:
        print(f"[COMMAND][RANDOM_TOPICS] - Error: {e}")

# Run the bot
bot_client.run_until_disconnected()
