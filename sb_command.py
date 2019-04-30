import discord

class Command:

    def __init__(self, name, func):
        self.name = name
        self.func = func
        
    async def run(self, client, message, db_acc):
        # Profile is a special exception, hacky, but, lazy
        if not isinstance(message.channel, discord.DMChannel) and self.name != "profile":
            await message.channel.send("(I see you're running this command in a server. Why not try DMing me?)")
        await self.func(client, message, db_acc)

    def channel_only(self):
        return False