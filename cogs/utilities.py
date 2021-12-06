import discord
from discord.ext import commands  # Again, we need this imported
from discord.commands import slash_command
from classes import Confirm
import time
from pastecord import create_document
from datetime import datetime

bot = discord.Bot()


class Utilities(commands.Cog):
    """A couple of simple commands."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        await message.edit(
            content=
            f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms"
        )

    @commands.command(name="setstatus")
    @commands.cooldown(rate=1, per=5)
    @commands.has_role(847994265974997002)
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Set the bot's status."""


        await self.bot.change_presence(activity=discord.Game(name=text))

        statusreply = discord.Embed(description="Done!")

        await ctx.send(embed=statusreply)


    @setstatus.error
    async def setstatus_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandOnCooldown):
            error = f"This command is on cooldown, try again after {round(error.retry_after)} seconds."
        elif isinstance(error, commands.MissingRole):
            error = discord.Embed(
                title="**Error!**",
                description=
                "```diff\n-<:GA_no:851965642318938122> - You don't have the permissions to use this command!```"
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            error = discord.Embed(
                title="**Error!**",
                description=
                f"```diff\n-<:GA_no:851965642318938122> - Missing an required argument!\n{error.param}\n- ^^^^^```"
            )
        else:
            error = "Oh no! Something went wrong while running the command!"

        await ctx.send(error, delete_after=5)
        await ctx.message.delete(delay=5)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(845454673263460395)

        if not channel:
            return

        await channel.send(f"Welcome, {member}!")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.command(name="snipe")
    async def _snipe(self, ctx: commands.Context):
        """A command to snipe delete messages."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            nomessage = discord.Embed(
                title="**Error!**",
                description="**```diff\n-There is no message to snipe!\n```**",
                timestamp=datetime.utcnow())
            await ctx.send(embed=nomessage)
            return

        author = self.last_msg.author
        content = self.last_msg.content

        stringembed = discord.Embed(title=f"Message from {author}",
                                    description=content)
        await ctx.send(embed=stringembed)

    @bot.slash_command(
        guild_ids=[845454672755425362],
        name="snipe",
        description="UTILITIES - A command to snipe delete messages.")
    async def snipe(self, ctx: commands.Context):
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            nomessage = discord.Embed(
                title="**Error!**",
                description="**```diff\n-There is no message to snipe!\n```**")
            await ctx.respond(embed=nomessage)
            return

        author = self.last_msg.author
        content = self.last_msg.content

        stringembed = discord.Embed(title=f"Message from {author}",
                                    description=content)
        await ctx.respond(embed=stringembed)

    @snipe.error
    async def snipe_error(ctx, error):
        if isinstance(error, commands.CommandError):

            snipeerror = discord.Embed(
                title="**ERROR!**",
                description=
                "```diff \n- An error occured while using this command.  ```")
            await ctx.respond(embed=snipeerror)

    @bot.slash_command(guild_ids=[845454672755425362],
                       name="hello",
                       description="UTILITIES - Testing for slash commands"
                       )  # Create a slash command for the supplied guilds.
    async def hello(self, ctx):
        await ctx.respond("Hi, this is a slash command from a cog!")

    @commands.command(name="say")
    async def _say(self, ctx: commands.Context, *, text: str):
        await ctx.send(message=text)
        await ctx.message.delete(delay=5)

    @commands.command(name="embed")
    async def _embed(self, ctx: commands.Context, *, text: str):
        embed = discord.Embed(color=0x56C9F0,
                              title=f"{ctx.author}",
                              description=text,
                              timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author.display_name,
                         icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        await ctx.message.delete(delay=5)

    @commands.command(name="pastecord")
    async def _pastecord(self, ctx: commands.Context, *, text: str):
        document = create_document(text)
        embed = discord.Embed(
            color=0x56C9F0,
            title="Success!",
            description=
            f"Your pastecord is located at this url: {document.url}",
            timestamp=datetime.utcnow())
        embed.set_author(
            name="Glacier Moderation",
            icon_url=
            "https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024"
        )
        embed.set_footer(text=f"Requested by {ctx.author}",
                         icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @_pastecord.error
    async def pastecord_error(ctx, error):
        if isinstance(error, commands.CommandError):
            error = discord.Embed(
                title="**ERROR!**",
                description=
                "```diff \n- An error occured while using this command.  ```")
            await ctx.respond(embed=error)



def setup(bot):
    bot.add_cog(Utilities(bot))
