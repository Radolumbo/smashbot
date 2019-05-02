import discord

class Command:

    def __init__(self, name, func):
        self.name = name
        self.func = func
        
    async def run(self, client, message, db_acc):
        await self.func(client, message, db_acc)

    def channel_only(self):
        return False