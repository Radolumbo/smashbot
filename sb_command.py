class Command:

    def __init__(self, name, func):
        self.name = name
        self.func = func

    def check(self, string):
        return string == self.name

    async def run(self, message, db):
        await self.func(message, db)

    async def check_and_run(self, string):
        if self.check(string):
            await self.run()