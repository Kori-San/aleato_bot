from dotenv import load_dotenv
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, Updater

import logging
import random
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from the environment variables
TOKEN = os.getenv("API_TOKEN")
if not TOKEN:
    raise ValueError("API_TOKEN not found in .env file")

CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
if not CHANNEL_USERNAME:
    raise ValueError("CHANNEL_USERNAME not found in .env file")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to check if a message has media content
def has_media(message):
    return message.photo or message.video or message.animation or message.audio

# Function to handle the /randomposts command
def random_posts(update: Update, context: CallbackContext) -> None:
    # Get all messages from the channel
    all_messages = context.bot.get_chat_history(chat_id=CHANNEL_USERNAME, limit=9999)  # Set a high limit

    # Filter messages with media content
    media_messages = [message for message in all_messages if has_media(message)]

    # Randomly select 10 media messages
    selected_media_messages = random.sample(media_messages, k=min(10, len(media_messages)))

  # Delete the bot's previous messages
    context.bot.delete_messages(chat_id=update.effective_chat.id, message_ids=update.effective_message.message_id)

    # Send the selected media messages to the user
    for message in selected_media_messages:
        context.bot.send_message(chat_id=update.effective_chat.id, text=message.text)

# Create a bot instance
bot = Bot(token=TOKEN)

# Set up the updater and dispatcher
updater = Updater(bot=bot, use_context=True)
dispatcher = updater.dispatcher

# Register the /randomposts command handler
dispatcher.add_handler(CommandHandler("randomposts", random_posts))

# Start the bot
updater.start_polling()

# Run the bot until you send a signal to stop it
updater.idle()
