import logging
import os
from dotenv import load_dotenv

import disnake
from disnake.ext import commands

import checks
import keep_alive

logging.basicConfig(level=logging.WARNING)

intents = disnake.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="=", intents=intents)

load_dotenv()

@bot.event
async def on_ready():
    print("\033[1;32m[STATUS] Logged in as {0.user}".format(bot))
    print("\033[1;32m[STATUS] Bot Ready! \u001b[0m\n")


# Load:
@bot.command()
@commands.check(checks.LEVEL_A)
async def load(ctx, extension):
    """
    Loads a cog.

    **Permission Requirement:**```ini
    [ A ] Level = "Owner"
    ```
    **Usage:**```md
    =load <extension>
    ```
    """
    bot.load_extension(f"{extension}")
    await ctx.send(f"Successfully loaded `{extension}`")


# Unload:
@bot.command()
@commands.check(checks.LEVEL_A)
async def unload(ctx, extension):
    """
    Unloads a cog.

    **Permission Requirement:**```ini
    [ A ] Level = "Owner"
    ```
    **Usage:**```md
    =unload <extension>
    ```
    """
    bot.unload_extension(f"{extension}")
    await ctx.send(f"Successfully unloaded `{extension}`")


# Add this after the load and unload commands
for filename in os.listdir(
    "cogs"
):  # import os in your code and also replace the 'cogs' with your folder name
    if filename.endswith(".py"):
        bot.load_extension(
            f"cogs.{filename[:-3]}"
        )  # replaces file extension('.py') and loads it


my_secret = os.getenv("TOKEN")
bot.run(my_secret)

keep_alive.keep_alive()
