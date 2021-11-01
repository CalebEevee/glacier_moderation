import discord
from discord.ext import commands
import os


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="=", intents=intents)

# Load:
@bot.command(aliases = ['l'])
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'{extension}')
    await ctx.send(f'Successfully loaded `{extension}`')
# Unload:
@bot.command(aliases = ['ul'])
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'{extension}')
    await ctx.send(f'Successfully unloaded `{extension}`')


# Add this after the load and unload commands
for filename in os.listdir('cogs'): # import os in your code and also replace the 'cogs' with your folder name
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}') # replaces file extension('.py') and loads it


bot.run("ODUyNzM2MDMzMTE5NTM1MTY0.YMLKUQ.h2WGyJZCEpJvbtEK_eowFjOa8js")


    

    



