import os
from dataclasses import dataclass
from discord import channel
from time import sleep
from aws import EC2


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
class StartMinecraft(Command):

    async def action(self):
        await self.channel_response.send('Starting minecraft server...')

        minecraft_instance = os.getenv('MINECRAFT_SERVER')
        self.run_instance(minecraft_instance)

        await self.channel_response.send('Minecraft server is running!')

    def run_instance(self, instance_id):

        ec2 = EC2(instance_id)

        if ec2.check_is_running():
            return

        ec2.start_instance()

        while True:
            if ec2.check_is_running():
                break
            sleep(5)


class StopMinecraft(Command):

    async def action(self):

        minecraft_instance = os.getenv('MINECRAFT_SERVER')
        ec2 = EC2(minecraft_instance)
        ec2.stop_instance()

        await self.channel_response.send('Minecraft server is Stopped!')


commands = {
    'SAY_HELLO': SayHello,
    'SAY_GOODBYE': SayGoodBye,
    'START_MINECRAFT': StartMinecraft,
    'STOP_MINECRAFT': StopMinecraft
}


@dataclass
class ShowMenu(Command):
    async def action(self):
        menulist = [f"{index + 1}. {key}" for index,
                    key in enumerate(commands.keys())]
        menulist = ["Menu: \n0. MENU"] + menulist
        menu_message = "\n".join(menulist)
        await self.channel_response.send(menu_message)


def run_command(user_command: str, channel_response: channel):
    print("Received command: ", user_command)

    if user_command == 'MENU':
        return ShowMenu(channel_response).action

    command: Command = commands.get(user_command)(channel_response)
    return command.action
