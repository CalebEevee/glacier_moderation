import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="=", intents=intents)


bot.load_extension("utilities") # Note, we don't need the .py file extension




bot.run("ODUyNzM2MDMzMTE5NTM1MTY0.YMLKUQ.h2WGyJZCEpJvbtEK_eowFjOa8js")


    

    



