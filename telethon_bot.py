import os
from telethon import TelegramClient, events, sync

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()

API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
ALLOWED_CHATS = [int(chat) for chat in os.getenv('ALLOWED_CHATS').split(',')]
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH')

with TelegramClient('max', API_ID, API_HASH) as client:
    client.send_message('me', 'Hello, myself!')

    @client.on(events.NewMessage(chats=ALLOWED_CHATS))
    async def handler(event):

        if event.message.media:
            title = event.message.text.strip()\
                .replace('\n', ' ').replace(' ', '_').replace('/', '-')

            await event.reply(f'Downloading file: {title}')
            await event.message.download_media(
                DOWNLOAD_PATH + title)
            await event.reply('Downloaded!')
            return

    client.run_until_disconnected()
