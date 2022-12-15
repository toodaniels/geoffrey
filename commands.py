from dataclasses import dataclass
from discord import channel

from asyncio import create_task


@dataclass
class Command:
    channel_response: channel


@dataclass
class SayHello(Command):
    async def action(self):
        await self.channel_response.send('Hello World!')


@dataclass
class SayGoodBye(Command):
    async def action(self):
        await self.channel_response.send('BYE!')


@dataclass
class ShowMenu(Command):
    async def action(self):
        pass


commands = {
    'SAY_HELLO': SayHello,
    'SAY_GOODBYE': SayGoodBye,
    'MENU': ShowMenu
}


def run_command(user_command: str, channel_response: channel):
    print("Received command: ", user_command)
    command: Command = commands.get(user_command)(channel_response)
    return command.action
