import discord
from discord.ext import commands

class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()

        helpembed = discord.Embed(title = "Glacier Moderation Help Menu",description = "Here is the list of commands!", colour=0x87CEEB)
        helpembed.set_author(name = "Glacier Moderation", icon_url = "https://images-ext-1.discordapp.net/external/_LmWpCrF4y2KYXdC3ssm4CSBgKhJxvpQy4i-6D03mSg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png")
        helpembed.add_field(name="Utilities", value="`help` \n `setstatus`\n `snipe` \n`ping`", inline=True)
        helpembed.add_field(name="Field 2", value="An inline field!", inline=True)
        helpembed.add_field(name="Field 3", value="Look I'm inline with field 2!", inline=True)  
        await channel.send(embed=helpembed)

class Helpcog(commands.Cog):
    def __init__(self, bot):
       self.bot = bot
        
       # Focus here
       # Setting the cog for the help
       help_command = MyHelp()
       help_command.cog = self # Instance of YourCog class
       bot.help_command = help_command


def setup(bot: commands.Bot):
    bot.add_cog(Helpcog(bot))
    