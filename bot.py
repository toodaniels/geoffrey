import os
import argparse

import discord

from dotenv import load_dotenv

load_dotenv()  # Loads envs from .env


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--message", required=True, help="Message content")
    return parser.parse_args()


def init_client() -> discord.Client:
    intents = discord.Intents.default()
    intents.message_content = True
    return discord.Client(intents=intents)


def send_message(client: discord.Client, message: str):
    @client.event
    async def on_ready():  # Called when internal cache is loaded
        # Gets channel from internal cache
        channel = client.get_channel(int(os.getenv('CHANNEL_ID')))
        await channel.send(message)  # Sends message to channel
        await client.close()  # Close connection
    return on_ready


def main() -> None:
    args = parse_args()
    print(type(args))
    client = init_client()
    print(type(send_message(client=client, message=args.message)))
    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == "__main__":
    main()
