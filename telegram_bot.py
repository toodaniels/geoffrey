import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def downloader(update, context):
    print('Receive a image')
    print(update.message.video)
    file = await context.bot.get_file(update.message.video)
    # await file.download_to_drive('image.png')

if __name__ == '__main__':

    application = ApplicationBuilder().token(
        os.getenv('TELEGRAM_BOT_TOKEN')).build()

    start_handler = CommandHandler('start', start)
    download_handler = MessageHandler(filters.ATTACHMENT, downloader)

    application.add_handler(start_handler)
    application.add_handler(download_handler)

    application.run_polling()