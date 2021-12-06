import discord
from discord.ext import commands
from discord.commands import slash_command 
import asyncio
import motor.motor_asyncio
import pprint
import re
import time
from pastecord import create_document
from datetime import datetime

class Staff(commands.Cog):
    """Staff Commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="strike")
    async def strike(self, ctx, member: discord.Member, *,reason):
        if not reason:
          await ctx.send("Please provide a reason!")
          return

        await ctx.send("This comamnd is not written(ready) yet!")

    @commands.group()
    async def staff(self, ctx):
    # Do nothing if a sub command is not invoked, you could also perhaps send the help message
        if not ctx.invoked_subcommand:
          return

    @staff.command(name="warn")
    async def _staff_warn(self, ctx, member: discord.Member, *, reason):
        if not reason:
          await ctx.send("Please provide a reason!")
          return

        document =  create_document(reason)
        embed = discord.Embed(color=0x56C9F0, title="Warning", description=f":warning: **`[ WARNING ]`** {member.mention} `[ {member.id} ]` [WARNING REASON]({document.url})", timestamp=datetime.utcnow())
        embed.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)


        channel = self.bot.get_channel(846880762641121361)
        channel2 = self.bot.get_channel(915046310804095036)

        if not channel:
            return

            
        message = f"```ini\n{member.id} has been given a staff"
        
        await channel.send(member.mention)
        await channel.send(embed=embed) 
        await channel2.send(message)
        await member.send(f"{member.mention}, You have been given a __staff warning__ in Glacier Advertising!\n The details are listed below!")
        await member.send(embed=embed)

    



def setup(bot):
    bot.add_cog(Staff(bot))
    

        

      


        
    

