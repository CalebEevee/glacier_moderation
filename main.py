import discord
from discord.ext import commands
import os
import logging
import keep_alive



logging.basicConfig(level=logging.WARNING)



intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="=", intents=intents)


@bot.event
async def on_ready():
    print('\033[1;32m[STATUS] Logged in as {0.user}'.format(bot))
    print("\033[1;32m[STATUS] Bot Ready! \u001b[0m\n")


# Load:
@bot.command(aliases = ['l'])
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'{extension}')
    await ctx.send(f'Successfully loaded `{extension}`')
# Unload:
@bot.command(aliases = ['ul'])
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'{extension}')
    await ctx.send(f'Successfully unloaded `{extension}`')



# Add this after the load and unload commands
for filename in os.listdir('cogs'): # import os in your code and also replace the 'cogs' with your folder name
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}') # replaces file extension('.py') and loads it



my_secret = os.environ['TOKEN']
bot.run(my_secret)

keep_alive.keep_alive()




    

    



