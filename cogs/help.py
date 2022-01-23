import disnake
from disnake.ext import commands

import classes

bot = commands.Bot(command_prefix="=")


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):

        channel = self.get_destination()
        embeds = [
            disnake.Embed(
                title="Welcome!",
                description="Welcome to the **Glacier Moderation Help Menu!**\n>Please use the buttons below to navigate this help menu!```yaml\n1: Welcome Page\n2: Utility Commands\n3: Staff Commands\n```",
                colour=0x56C9F0,
            ),
            disnake.Embed(
                title="Page 2",
                description='```ini\n[ Utility Commands ]\n``````The letters in brackets indicate which permission level is required to execute the command.\nNormal members are located under the level W.```\n```ini\n[Z] Ping = "Get the ping and latency"\n[Z] Snipe = "Get the last deleted message in the channel"\n```',
                colour=0x56C9F0,
            ),
            disnake.Embed(
                title="Paginator example",
                description="This is the third embed.",
                colour=0x56C9F0,
            ),
        ]
        embeds[0].set_footer(text=f"Page 1 of {len(embeds)}")
        await channel.send(embed=embeds[0], view=classes.Menu(embeds))


class YourCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        help_command = MyHelp()
        help_command.cog = self  # Instance of YourCog class
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(YourCog(bot))
