from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CommandHandler, CallbackContext

import logging
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the token from the environment variables
TOKEN = os.getenv("API_TOKEN")
if not TOKEN:
    raise ValueError("API_TOKEN not found in .env file")

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Log the TOKEN
logger.info(f"TOKEN: {TOKEN}")

async def hello(update: Update, context: CallbackContext) -> None:
    """Send a salutation when the user sends /hello."""
    user_id = update.message.from_user.id
    text = '👋 Greetings !\n\nMy name is Aléato !'

    await context.bot.send_message(user_id, text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add the /hello command handler
    application.add_handler(CommandHandler("hello", hello))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
