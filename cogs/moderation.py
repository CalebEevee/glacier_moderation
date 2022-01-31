import asyncio
import pprint
import re
from datetime import datetime

import disnake
import motor.motor_asyncio
from disnake.ext import commands

today = datetime.now()

import os
from dotenv import load_dotenv

bot = commands.Bot(command_prefix=">")

load_dotenv()


connection_url = os.getenv("MONGO_URI")
client = motor.motor_asyncio.AsyncIOMotorClient(str(connection_url))
db = client["moderation"]
warning_collection = db["warnings"]
modlog_collection = db["modlog"]

print("\u001b[1;32m[STATUS] Initialized Database \u001b[0m")


# start code for mute command

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k)
                )
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


# moderation start


class Moderation(commands.Cog):
    """Moderation Commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_any_role(846502340017913907, 846503865775030323)
    async def ban(self, ctx, member: disnake.Member, *, reason="No reason given."):
        """Ban a user!"""
        author = ctx.author
        if member == None or member == ctx.message.author:
            await ctx.channel.send("You cannot ban yourself")
            return
        message = await ctx.send(f"Are you sure you want to ban {member}?")
        check = lambda m: m.author == ctx.author and m.channel == ctx.channel

        if member.guild_permissions.administrator and member != None:
            embed = disnake.Embed(
                color=disnake.Colour.red(),
                title="Administrator",
                description="This user is an administrator and is not allowed to be banned.",
            )
            await ctx.send(embed=embed)
            return

        if reason == None:
            embed1 = disnake.Embed(
                color=disnake.Colour.red(),
                title="Reason Required!",
                description="You must enter a reason to ban this member.",
            )
            await ctx.send(embed=embed1)
            return

        try:
            confirm = await self.bot.wait_for("message", check=check, timeout=30)
        except asyncio.TimeoutError:
            await message.edit(content="Ban cancelled, timed out.")
            return

        if confirm.content == "yes":
            dm = disnake.Embed(
                title="**You have been banned!**",
                description=f"You have been **banned** from {ctx.guild.name}! **```diff\n-{reason} \n```**",
            )
            log = disnake.Embed(
                color=disnake.Colour.green,
                title="**Ban**",
                description=f"`Username`:{member}\n`User ID:`{member.id}\n`Moderator:`{author.mention}\n`Reason:`{reason}",
            )

            channel = self.bot.get_channel(908474591230443580)

            modlog_collection.insert_one(
                {
                    "Type": "BAN",
                    "User-ID:": (member.id),
                    "Moderator-ID:": (author.id),
                    "Reason:": "(reason)",
                    "Date:": (today),
                }
            )

            await message.edit(content=f"{member} has been banned.")
            await member.send(embed=dm)
            await channel.send(embed=log)
            await member.ban(member, reason=reason)

            return

        await message.edit(content="Ban cancelled.")

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: disnake.Member, *, time: TimeConverter = None):
        """Mutes a member for the specified time- time in 2d 10h 3m 2s format ex:
        &mute @Someone 1d"""
        role = disnake.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(
            ("Muted {} for {}s" if time else "Muted {}").format(member, time)
        )
        if time:
            await asyncio.sleep(time)
            await member.remove_roles(role)

    @commands.command(pass_context=True)
    @commands.has_any_role(853391228409085962)
    async def warn(self, ctx, member: disnake.Member, *, reason):
        if member.id in [ctx.author.id, self.bot.user.id]:
            return await ctx.send("**Error! You cannot ban yourself or the bot!**")

        author = ctx.author
        if not reason:
            await ctx.send("Please provide a reason")
            return

        reason.strip()

        # CHANNEL CONFIRM
        await ctx.send(
            f"**<:GA_yes:851965019045494804> - {member.name} [{member.id}] has been warned by {author.name}.**"
        )
        # MEMBER DM
        await member.send(
            f"You have been warned in **{ctx.guild.name}** by **{author.name}**."
        )
        # MODLOG-DB
        await modlog_collection.insert_one(
            {
                "Type": "WARN",
                "User-ID:": (member.id),
                "Moderator-ID:": (author.id),
                "Reason:": f"{reason}",
                "Date:": (today),
            }
        )
        # WARNING DB
        await warning_collection.insert_one(
            {
                "Type": "WARN",
                "User-ID:": (member.id),
                "Moderator-ID:": (author.id),
                "Reason:": f"{reason}",
                "Date:": (today),
            }
        )
        # SERVER MODLOG
        log = disnake.Embed(
            colour=0x56C9F0,
            title="**Warning**",
            description=f"`Username`: {member}\n`User ID:` {member.id}\n`Moderator:`{ author.mention}\n`Reason:` {reason}",
        )

        channel = self.bot.get_channel(908474591230443580)

        await channel.send(embed=log)

    @commands.command(name="warnings")
    @commands.has_any_role(853391228409085962)
    async def warnings(self, ctx, member: disnake.Member):

        n = await warning_collection.count_documents({"User-ID:": (member.id)})

        cursor = warning_collection.find({"User-ID:": (member.id)}).sort("Date:")
        for document in await cursor.to_list(length=100):
            pprint.pformat(document)
            pprint.pprint(document)

            embed = disnake.Embed(
                colour=0x56C9F0,
                title="Warning List",
                description="This is the list of warnings for the requested user.",
            )
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar.url
            )
            embed.add_field(name="USER ID", value=f"`[ {member.id} ]`", inline=True)
            embed.add_field(name="Number of Warnings", value=n, inline=True)
            embed.add_field(
                name="Warning List", value=f"```{document}```", inline=False
            )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
