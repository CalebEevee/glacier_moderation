import disnake
from disnake.ext import commands


class Blacklist(commands.Cog):
    """Blacklist commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def blacklist(ctx):
        if ctx.author.id == id:
            return False
        return True
