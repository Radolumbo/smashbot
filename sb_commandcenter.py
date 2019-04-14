from sb_command import * 

class CommandCenter:

    commands = {}

    def __init__(self):
        pass

    def register_command(self, name, func):
        command = Command(name, func)
        self.commands[name] = command

    async def run_command(self, name, message, db):
        if name in self.commands:
            await self.commands[name].run(message, db)
            return True

        return False