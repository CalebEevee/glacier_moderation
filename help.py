from discord.ext import commands

bot = commands.Bot(command_prefix="=")

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        await channel.send("hello!")

bot.help_command = MyHelp()