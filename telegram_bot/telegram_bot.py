import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from telegram.ext import CallbackContext

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('START')
    await update.message.reply_text("Presionaste Start")


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('download')
    await update.message.reply_text("Descargando")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


if __name__ == '__main__':

    application = ApplicationBuilder().token(
        os.getenv('TELEGRAM_BOT_TOKEN')).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.ATTACHMENT, download_video))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()
