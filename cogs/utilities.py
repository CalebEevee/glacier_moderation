import discord
from discord.ext import commands # Again, we need this imported
import time
from discord import Member


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

        await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(name="setstatus")
    @commands.cooldown(rate=1, per=5)
    async def setstatus(self, ctx: commands.Context, *, text: str):
        """Set the bot's status."""
        await self.bot.change_presence(activity=discord.Game(name=text))

        statusreply = discord.Embed(description = "Done!")

        await ctx.send(embed=statusreply)

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
    async def snipe(self, ctx: commands.Context):
        """A command to snipe delete messages."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content

        stringembed = discord.Embed(title=f"Message from {author}", description=content)
        await ctx.send(embed=stringembed)
    
    


        



# Now, we need to set up this cog somehow, and we do that by making a setup function:
def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))