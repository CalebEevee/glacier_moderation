import disnake
from disnake.ext import commands



class Confirm(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None


    @disnake.ui.button(label="Confirm", style=disnake.ButtonStyle.blurple)
    async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.message.delete()
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @disnake.ui.button(label="Cancel", style=disnake.ButtonStyle.grey)
    async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
      
            
        embed = disnake.Embed(title="Cancelled", description="<:GA_no:851965642318938122> You have cancelled this command!", color=0xFF0000)
        embed.set_author(name="Glacier Moderation", icon_url="https://cdn.discordapp.com/avatars/851592943075721268/58549a661b24ec550d5091a11599a030.png?size=1024")
        embed.set_footer(text=f"Requested by {interaction.author}", icon_url = interaction.author.avatar.url)
        await interaction.message.edit(embed=embed)


        for child in self.children:
          if isinstance(child, disnake.ui.Button):
                child.disabled = True
          
        await interaction.response.edit_message(view=self)
      
        self.value = False
        self.stop()





