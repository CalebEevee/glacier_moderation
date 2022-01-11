import disnake
from disnake.ext import commands
from typing import List

bot = commands.Bot(command_prefix="=")


class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        Menu()


class Menu(disnake.ui.View):
    def __init__(self, embeds: List[disnake.Embed]):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.embed_count = 0

    @disnake.ui.button(emoji="⬅", style=disnake.ButtonStyle.blurple)
    async def next_page(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        if self.embed_count != 0:
            self.embed_count -= 1
            embed = self.embeds[self.embed_count]
            embed.set_footer(text=f"Page {self.embed_count + 1} of {len(self.embeds)}")
            await interaction.response.edit_message(embed=embed)

    @disnake.ui.button(emoji="➡", style=disnake.ButtonStyle.blurple)
    async def last_page(
        self, button: disnake.ui.Button, interaction: disnake.MessageInteraction
    ):
        if self.embed_count != (len(self.embeds) - 1):
            self.embed_count += 1
            embed = self.embeds[self.embed_count]
            embed.set_footer(text=f"Page {self.embed_count + 1} of {len(self.embeds)}")
            await interaction.response.edit_message(embed=embed)


class YourCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mycmd(self, ctx: commands.Context):
        embeds = [
            disnake.Embed(
                title="Paginator example",
                description="This is the first embed.",
                colour=disnake.Colour.random(),
            ),
            disnake.Embed(
                title="Paginator example",
                description="This is the second embed.",
                colour=disnake.Color.random(),
            ),
            disnake.Embed(
                title="Paginator example",
                description="This is the third embed.",
                colour=disnake.Color.random(),
            ),
        ]
        embeds[0].set_footer(text=f"Page 1 of {len(embeds)}")
        await ctx.send(embed=embeds[0], view=Menu(embeds))

        help_command = MyHelp()
        help_command.cog = self  # Instance of YourCog class
        bot.help_command = help_command


def setup(bot):
    bot.add_cog(YourCog(bot))
