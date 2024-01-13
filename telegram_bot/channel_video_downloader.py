import os
import sys
import re
from telethon import TelegramClient, events, sync
import textwrap

from dataclasses import dataclass

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()


@dataclass
class TelegramChannelVideoDownloader:
    session: str
    download_path: str
    API_ID: int = int(os.getenv('API_ID', '0'))
    API_HASH: str = os.getenv('API_HASH', '')
    BOT_TOKEN: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    ID_CHANNEL: str = os.getenv('', '')

    def __post_init__(self):
        self.client = TelegramClient(
            self.session, self.API_ID, self.API_HASH)
        self.bot_client = TelegramClient(
            'geoffrey', self.API_ID, self.API_HASH).start(bot_token=self.BOT_TOKEN)

    def download_progress(self, received_bytes, total):
        bar_length = 20
        percent = float(received_bytes) / total
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(
            hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def send_status_message(self, message):
        with self.bot_client as client:
            client.send_message('toodaniels', message)
    
    def define_file_name(self, title):
        title = title.strip()\
            .replace('\n', ' ').replace(' ', '_').replace('/', '-')\
            .replace('YameteKudasaiikuuuuu', '')\
            .replace('Latino', '') 
        
        title = re.sub(r'[^a-zA-Z0-9._-]', '_', title)
        title = re.sub(r'_+', '_', title)
        
        title = title[1:-1] + '.mp4'


        # patron = re.compile(r'Temporada_(\d+)_(\d+)-(\d+)_')
        # coincidencia = patron.search(title)

        # if coincidencia:
        #     numero_temporada = coincidencia.group(1)
        #     episodio_inicio = coincidencia.group(2)
        #     episodio_fin = coincidencia.group(3)
            
        #     print(f"Número de Temporada: {numero_temporada}")
        #     print(f"Episodio Inicio: {episodio_inicio}")
        #     print(f"Episodio Fin: {episodio_fin}")
        # else:
        #     print("El formato del texto no coincide con el esperado.")
        
        return title

    def download_message_media(self, message):
        title = self.define_file_name(message.text)
        self.send_status_message(f'Downloading {title}')
        print(f'\nDownloading {title}')
        message.download_media(
            self.download_path + title,
            progress_callback=self.download_progress
        )
        self.send_status_message(f'Downloaded {title}')

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
    
    def search_message_by_text(self, chat_id, text):
        with self.client as client:
            messages = client.get_messages(chat_id, search=text, limit=10)

            if len(messages) > 1: 
                raise ValueError(
                    f'{len(messages)} matches of messages were found.')

            message = messages.pop()
            message_id = message.id
            message_text = textwrap.shorten(
                message.text, width=30, placeholder="...")
            
            print(f'ID Message found: {message_id} with text: {message_text}')
            return message_id



def main():
    chat_id = sys.argv[1]
    limit = int(sys.argv[2])
    seach_text = sys.argv[3]

    downloader = TelegramChannelVideoDownloader(
        session='max',
        download_path=os.getenv('DOWNLOAD_PATH'))
    
    message_id = downloader.search_message_by_text(
        chat_id, text=seach_text)
    
    downloader.download_messages(chat_id, limit=limit, min_id=message_id)

if __name__ == '__main__':
    main()

 