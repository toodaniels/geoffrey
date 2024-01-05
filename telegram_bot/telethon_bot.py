import os
import asyncio
import logging
from telethon import TelegramClient, events

from telegram_bot.utils import convert_channel

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
ALLOWED_CHATS = os.getenv('ALLOWED_CHATS', []).split(',')
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

client = TelegramClient(
    'geoffrey', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


with client:
    @client.on(
        events.NewMessage(chats=list(map(convert_channel, ALLOWED_CHATS))))
    async def handler(event):
        logging.info("New Message received!")
        if event.message.media:
            
            logging.info("The message have media")
            title = event.message.text.strip()\
                .replace('\n', ' ').replace(' ', '_').replace('/', '-')
            title = re.sub(r'[^a-zA-Z0-9._-]', '_', title)
            title = re.sub(r'_+', '_', title)

            await event.reply(f'Downloading file: {title}')
            download_filename = DOWNLOAD_PATH + title
            await event.message.download_media(download_filename)
            await event.reply(f'Downloaded!')
            return

    client.run_until_disconnected()
