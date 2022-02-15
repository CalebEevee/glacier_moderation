import disnake
from disnake.ext import commands


class ErrorHandler(commands.Cog):
    """A cog for global error handling."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener
    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ):
        """Global Error Handler"""
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"This commands is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissino to run this command!"
        elif isinstance(error, commands.UserInputError):
            message = "Something about your input was wrong, please check your input and try again!"
        else:
            message = "Oh no! Something went wrong while running this command!"

        eembed = disnake.Embed(
            title="Error!",
            description=f"An error occured while running this command!\n```diff\n- {message}\n```",
        )

        await ctx.send(embed=eembed, content=ctx.message.author.mention)


def setup(bot: commands.Bot):
    bot.add_cog(ErrorHandler(bot))
