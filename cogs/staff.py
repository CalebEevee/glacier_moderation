import disnake
from disnake.ext import commands
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



    @commands.group()
    async def staff(self, ctx):
    # Do nothing if a sub command is not invoked, you could also perhaps send the help message
        if not ctx.invoked_subcommand:
          return

    @staff.command(name="warn")
    async def _staff_warn(self, ctx, member: disnake.Member, *, reason):
        if not reason:
          await ctx.send("Please provide a reason!")
          return

        document =  create_document(reason)
        embed = disnake.Embed(color=0x56C9F0, title="Warning", description=f":warning: **`[ WARNING ]`** {member.mention} `[ {member.id} ]` [**WARNING REASON PASTEBIN**]({document.url})", timestamp=datetime.utcnow())
        embed.add_field(name="Warning Reason", value=f"```fix\n{reason}\n```", inline="false")
        embed.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)


        channel = self.bot.get_channel(846880762641121361)
        channel2 = self.bot.get_channel(915046310804095036)

        if not channel:
            return

        if not channel2:
            return

        await ctx.send(f"{ctx.author.mention} Done!")
        await channel.send(member.mention,embed=embed)
        await channel2.send(embed=embed)
        await member.send(f"{member.mention}, You have been given a __staff warning__ in Glacier Advertising!\n The details are listed below!")
        await member.send(member.mention, embed=embed)




    @staff.command(name="strike")
    async def _staff_strike(self, ctx, member: disnake.Member, *, reason):
        if not reason:
          await ctx.send("Please provide a reason!")
          return

        document =  create_document(reason)
        embed = disnake.Embed(color=0x56C9F0, title="Strike", description=f":triangular_flag_on_post: **`[ STRIKE ]`** {member.mention} `[ {member.id} ]` [**STRIKE REASON PASTEBIN**]({document.url})", timestamp=datetime.utcnow())
        embed.add_field(name="Strike Reason", value=f"```fix\n{reason}\n```", inline="false")
        embed.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)




        channel = self.bot.get_channel(846880762641121361)
        channel2 = self.bot.get_channel(915046310804095036)

        if not channel:
            return

        if not channel2:
            return



        await ctx.send(f"{ctx.author.mention} Done!")
        await channel.send(member.mention,embed=embed)
        await channel2.send(embed=embed)
        await member.send(f"{member.mention}, You have been given a __staff strike__ in Glacier Advertising!\n The details are listed below!")
        await member.send(member.mention, embed=embed)


    @staff.command(name="log-demote")
    async def _staff_log_demote(self, ctx, member: disnake.Member, oldrole: disnake.Role, newrole: disnake.Role ,*, reason):

        if not reason:
          await ctx.send("Please provide a reason!")
          await ctx.send("```css\n=staff log-demote <oldrole> <newrole> <reason>\n```")
          return
        
        if not oldrole:
          await ctx.send("Please provide an old role!")
          await ctx.send("```css\n=staff log-demote <oldrole> <newrole> <reason>\n```")

        if not newrole:
          await ctx.send("Please provide a new role!")
          await ctx.send("```css\n=staff log-demote <oldrole> <newrole> <reason>\n```")

        document =  create_document(reason)
        embed = disnake.Embed(color=0xffc16b, title="Demotion", description=f":small_red_triangle_down: **`[ DEMOTION ]`** {member.mention} `[ {member.id} ]` [**DEMOTION REASON PASTEBIN**]({document.url})", timestamp=datetime.utcnow())
        embed.add_field(name="Old Role", value=f"` {oldrole}  `", inline="true")
        embed.add_field(name="New Role", value=f"` {newrole}  `", inline="true")
        embed.add_field(name="Demotion Reason", value=f"```fix\n{reason}\n```", inline="false")
        embed.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)

        embed2=disnake.Embed(color=0xf75262, title="Demoted", description= ":small_red_triangle_down: This staff member has been __DEMOTED__.", timestamp=datetime.utcnow())
        embed2.add_field(name="<:GA_Member:920077003842019338> Member", value=f"{member.mention}", inline="true")
        embed2.add_field(name="<:GA_ID:920101219215745025> Member ID", value=f"**`[{member.id}]`**", inline = "true")
        embed2.add_field(name="<:GA_Ban:920078316067762266> Approval", value=f"{ctx.author.mention}\n**`[{ctx.author.id}]`**", inline="true")
        

        embed2.add_field(name="Demotion Reason", value=f"```fix\n{reason}\n```", inline="false")
        embed2.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed2.set_thumbnail(url="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/48164/tomato-emoji-clipart-sm.png")
        embed2.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)


        logchannel = self.bot.get_channel(899809959670333440)
        channel2 = self.bot.get_channel(920055632684515369)

        if not logchannel:
            return

        if not channel2:
            return



        await ctx.send(f"{ctx.author.mention} Done!")
        await logchannel.send(member.mention,embed=embed)
        await channel2.send(embed=embed)
        await member.send(f"{member.mention}, You have been __demoted__ in Glacier Advertising!\n The details are listed below!")
        await member.send(member.mention, embed=embed)



    

    @staff.command(name="log-fire")
    async def _staff_log_fire(self, ctx, member: disnake.Member, *, reason):

        if not reason:
          await ctx.send("Please provide a reason!")
          await ctx.send("```css\n=staff log-fire <reason>\n```")
          return
        


        embed2=disnake.Embed(color=0xf75262, title="Fired", description= ":tomato: This staff member has been __FIRED__.", timestamp=datetime.utcnow())
        embed2.add_field(name="<:GA_Member:920077003842019338> Member", value=f"{member.mention}", inline="true")
        embed2.add_field(name="<:GA_ID:920101219215745025> Member ID", value=f"**`[{member.id}]`**", inline = "true")
        embed2.add_field(name="<:GA_Ban:920078316067762266> Approval", value=f"{ctx.author.mention}\n**`[{ctx.author.id}]`**")
        embed2.add_field(name="Firing Reason", value=f"```fix\n{reason}\n```", inline="false")
        embed2.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed2.set_thumbnail(url="https://creazilla-store.fra1.digitaloceanspaces.com/emojis/48164/tomato-emoji-clipart-sm.png")
        embed2.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar.url)






        logchannel = self.bot.get_channel(899809959670333440)
        channel2 = self.bot.get_channel(920055632684515369)

        if not logchannel:
            return

        if not channel2:
            return



        await ctx.send(f"{ctx.author.mention} Done!")
        await logchannel.send(member.mention,embed=embed2)
        await channel2.send(embed=embed2)
        await member.send(f"{member.mention}, You have been __fired__ in Glacier Advertising!\n The details are listed below!")
        await member.send(member.mention, embed=embed2)

def setup(bot):
    bot.add_cog(Staff(bot))
    

        

      


        
    

