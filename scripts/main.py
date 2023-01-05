import os
import discord
from commands import run_command

if os.getenv('DEVELOPMENT'):
    from dotenv import load_dotenv
    load_dotenv()

ALLOWED_CHANNELS = [
    'second-channel'
]


class MyClient(discord.Client):
    async def on_ready(self):
        channel = self.get_channel(int(os.getenv('CHANNEL_ID')))
        # await channel.send("I'm ready to dance!")
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

        if message.author == self.user:
            return

        if str(message.channel) not in ALLOWED_CHANNELS:
            return

        if message.content.startswith('$geoffrey'):
            content_split = message.content.split(' ')
            user_command = content_split[1]
            action = run_command(user_command, message.channel)
            await action()


def bot_start():
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    bot_start()
