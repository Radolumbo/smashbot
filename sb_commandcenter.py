from sb_command import * 
from sb_constants import *

import discord

class CommandCenter:

    commands = {}

    def __init__(self):
        pass

    def register_command(self, command):
        self.commands[command.name] = command

    async def run_command(self, name, client, message, db):
        if name.lower() in self.commands:
            command = self.commands[name.lower()]
            if isinstance(message.channel, discord.DMChannel) and command.channel_only():
                return RC_CHANNEL_ONLY
            await command.run(client, message, db)
            return RC_SUCCESS

        return RC_COMMAND_DNE