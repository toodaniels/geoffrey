import os
import sys
from telethon import TelegramClient, events, sync

from dataclasses import dataclass

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()


@dataclass
class TelegramChannelVideoDownloader:
    session: str
    download_path: str
    API_ID = int(os.getenv('API_ID'))
    API_HASH = os.getenv('API_HASH')\


    def __post_init__(self):
        self.client = TelegramClient(
            self.session, self.API_ID, self.API_HASH)

    def download_progress(self, received_bytes, total):
        bar_length = 20
        percent = float(received_bytes) / total
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(
            hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def download_message_media(self, message):
        title = message.text.strip()\
            .replace('\n', ' ').replace(' ', '_').replace('/', '-')

        print(f'Downloading {title}')
        message.download_media(
            self.download_path + title,
            progress_callback=self.download_progress
        )

    def download_messages(self, chat_id, limit=200, min_id=None):
        with self.client as client:
            messages = client.get_messages(
                chat_id, limit=limit, min_id=min_id, reverse=True)
            list(map(self.download_message_media, messages))

    def download_message(self, chat_id, ids):
        with self.client as client:
            message = client.get_messages(
                chat_id, ids)

            self.download_message_media(message.pop())


def main():
    downloader = TelegramChannelVideoDownloader(
        session='max',
        download_path=os.getenv('DOWNLOAD_PATH'))

    downloader.download_messages(1772208943, limit=2, min_id=81)


if __name__ == '__main__':
    main()
