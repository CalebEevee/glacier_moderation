import discord
from discord.ext import commands
import asyncio
import motor.motor_asyncio

from datetime import date
today = date.today()

import os


connection_url = os.environ['MONGO_URI']
client = motor.motor_asyncio.AsyncIOMotorClient(str(connection_url))
db = client['moderation']
warning_collection = db['warnings']
modlog_collection = db['modlog']
print("Initialized Database\n-----")






class Moderation(commands.Cog):
    """Moderation Commands"""
    def __init__(self, bot: commands.Bot):
       self.bot = bot
     
    @commands.command(name="ban")
    @commands.has_any_role(846502340017913907, 846503865775030323)
    async def ban(self, ctx, member: discord.Member, *, reason= "No reason given."): 
        """Ban a user!"""
        author = ctx.author
        if member == None or member == ctx.message.author:
          await ctx.channel.send("You cannot ban yourself")
          return
        message = await ctx.send(f"Are you sure you want to ban {member}?")
        check = lambda m: m.author == ctx.author and m.channel == ctx.channel
        
        if member.guild_permissions.administrator and member != None:
          embed=discord.Embed(color=discord.Colour.red(), title="Administrator", description="This user is an administrator and is not allowed to be banned.")
          await ctx.send(embed=embed)
          return

        if reason == None:
          embed1=discord.Embed(color=discord.Colour.red(), title="Reason Required!", description="You must enter a reason to ban this member.")      
          await ctx.send(embed=embed1)
          return

        
        try:
            confirm = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.edit(content="Ban cancelled, timed out.")
            return
        
        if confirm.content == "yes":
            dm =  discord.Embed(title="**You have been banned!**", description=f"You have been **banned** from {ctx.guild.name}! **```diff\n-{reason} \n```**")
            log = discord.Embed(color=discord.Colour.green,title="**Ban**", description=f"`Username`:{member}\n`User ID:`{member.id}\n`Moderator:`{author.mention}\n`Reason:`{reason}")

            channel = self.bot.get_channel(908474591230443580)

            
            modlog_collection.insert_one({"Type":"BAN","User-ID:":(member.id),"Moderator-ID:":(author.id), "Reason:":"(reason)","Date:":(today)})



            await message.edit(content=f"{member} has been banned.")
            await member.send(embed=dm)
            await channel.send(embed=log)
            await member.ban(member, reason=reason)

            return

        await message.edit(content="Ban cancelled.")

    @commands.command(pass_context = True)
    @commands.has_any_role()
    async def warn(self, ctx, member:discord.Member, *,reason):
      if member.id in [ctx.author.id,self.bot.user.id]:
        return await ctx.send("**Error! You cannot ban yourself or the bot!**")
      
      author = ctx.author
      member = ctx.member
      if not reason:
        await ctx.send("Please provide a reason")
        return
      reason = ' '.join(reason)


      await ctx.send(f'**{member.mention} has been warned by {author.name}.**')

      await member.send(f'You have been warned in **{ctx.guild.name}** by **{author.name}**.')

      await modlog_collection.insert_one({"Type":"WARN","User-ID:":(member.id),"Moderator-ID:":(author.id), "Reason:":"(reason)","Date:":(today)})

      await warning_collection.insert_one({"Type":"WARN","User-ID:":(member.id),"Moderator-ID:":(author.id), "Reason:":"(reason)","Date:":(today)})

      log = discord.Embed(color=discord.Colour.blue,title="**Warning**", description=f"`Username`:{member}\n`User ID:`{member.id}\n`Moderator:`{author.mention}\n`Reason:`{reason}")

      channel = self.bot.get_channel(908474591230443580)

      await channel.send(embed=log)




      



def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot))       
       
       
             
      




