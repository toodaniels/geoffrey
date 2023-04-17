import os
import asyncio
from telethon import TelegramClient, events

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
ALLOWED_CHATS = os.getenv('ALLOWED_CHATS').split(',')
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

client = TelegramClient(
    'geoffrey', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


def convert_channel(id):
    try:
        return int(id)
    except Exception as e:
        return id


with client:

    @client.on(events.NewMessage(chats=list(map(convert_channel, ALLOWED_CHATS))))
    async def handler(event):
        print("New Message received!")

        if event.message.media:
            title = event.message.text.strip()\
                .replace('\n', ' ').replace(' ', '_').replace('/', '-')

            await event.reply(f'Downloading file: {title}')
            await event.message.download_media(
                DOWNLOAD_PATH + title)
            await event.reply('Downloaded!')
            return

    client.run_until_disconnected()
