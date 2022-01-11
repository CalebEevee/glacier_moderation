import disnake
from disnake.ext import commands

"""
Let users assign themselves roles by clicking on Buttons.
The view made is persistent, so it will work even when the bot restarts.
See this example for more information about persistent views
https://github.com/Pycord-Development/pycord/blob/master/examples/views/persistent.py
Make sure to load this cog when your bot starts!
"""

# this is the list of role IDs that will be added as buttons.
ping_role_ids = [853657348290772993, 853657556684505130, 853657678324826112]

color_role_ids = [
    853658889295101986,
    853659023001124905,
    853659105726300180,
    853659183638904842,
    853659429853069362,
    853659493811224587,
    853659577932054528,
    853659631121334363,
    853659797914910760,
    853659960307089408,
]


class RoleButton(disnake.ui.Button):
    def __init__(self, role: disnake.Role):
        """
        A button for one role. `custom_id` is needed for persistent views.
        """
        super().__init__(
            label=role.name,
            style=disnake.enums.ButtonStyle.primary,
            custom_id=str(role.id),
        )

    async def callback(self, interaction: disnake.Interaction):
        """This function will be called any time a user clicks on this button
        Parameters
        ----------
        interaction : disnake.Interaction
            The interaction object that was created when the user clicked on the button
        """

        # figure out who clicked the button
        user = interaction.user
        # get the role this button is for (stored in the custom ID)
        role = interaction.guild.get_role(int(self.custom_id))

        if role is None:
            # if this role doesn't exist, ignore
            # you can do some error handling here
            return

        # passed all checks
        # add the role and send a response to the uesr ephemerally (hidden to other users)
        if role not in user.roles:
            # give the user the role if they don't already have it
            await user.add_roles(role)
            await interaction.response.send_message(
                f"🎉 You have been given the role {role.mention}", ephemeral=True
            )
        else:
            # else, take the role from the user
            await user.remove_roles(role)
            await interaction.response.send_message(
                f"❌ The {role.mention} role has been taken from you", ephemeral=True
            )


class ButtonRoleCog(commands.Cog):
    """A cog with a slash command for posting the message with buttons
    and to initialize the view again when the bot is restarted
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def post(self, ctx):
        # Do nothing if a sub command is not invoked, you could also perhaps send the help message
        if not ctx.invoked_subcommand:
            return

    # make sure to set the guild ID here to whatever server you want the buttons in
    @commands.slash_command(
        guild_ids=[845454672755425362],
        name="post-button-role-pings",
        description="Post the button role message",
    )
    async def postbuttonpings(self, ctx: commands.Context):
        """Slash command to post a new view with a button for each role"""

        # timeout is None because we want this view to be persistent
        view = disnake.ui.View(timeout=None)

        # loop through the list of roles and add a new button to the view for each role
        for role_id in ping_role_ids:
            # get the role the guild by ID
            role = ctx.guild.get_role(role_id)
            view.add_item(RoleButton(role))
            embed = disnake.Embed(
                title="**__PING ROLES__**,",
                description="**`[ Click a button to assign yourself a role ]`**",
            )

        await ctx.send(embed=embed, view=view)

    @post.command(name="button-role-pings")
    async def _postbuttonpings(self, ctx: commands.Context):
        """Regular command to post a new view with a button for each role"""

        # timeout is None because we want this view to be persistent
        view = disnake.ui.View(timeout=None)

        # loop through the list of roles and add a new button to the view for each role
        for role_id in ping_role_ids:
            # get the role the guild by ID
            role = ctx.guild.get_role(role_id)
            view.add_item(RoleButton(role))
            embed = disnake.Embed(
                title="**__PING ROLES__**,",
                description="**`[ Click a button to assign yourself a role ]`**",
            )

        await ctx.send(embed=embed, view=view)

    @post.command(name="button-role-colors")
    async def _postbuttoncolors(self, ctx: commands.Context):
        """Regular command to post a new view with a button for each role"""

        # timeout is None because we want this view to be persistent
        view = disnake.ui.View(timeout=None)

        # loop through the list of roles and add a new button to the view for each role
        for role_id in color_role_ids:
            # get the role the guild by ID
            role = ctx.guild.get_role(role_id)
            view.add_item(RoleButton(role))
            embed = disnake.Embed(
                title="**__COLOR ROLES__**,",
                description="**`[ Click a button to assign yourself a role ]`**",
            )

        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_ready(self):
        """This function is called every time the bot restarts.
        If a view was already created before (with the same custom IDs for buttons)
        it will be loaded and the bot will start watching for button clicks again.
        """

        # we recreate the view as we did in the /post command
        view = disnake.ui.View(timeout=None)
        # make sure to set the guild ID here to whatever server you want the buttons in
        guild = self.bot.get_guild(845454672755425362)
        for role_id in ping_role_ids:
            role = guild.get_role(role_id)
            view.add_item(RoleButton(role))

        for role_id in color_role_ids:
            role = guild.get_role(role_id)
            view.add_item(RoleButton(role))

        # add the view to the bot so it will watch for button interactions
        self.bot.add_view(view)


def setup(bot):
    # load the cog
    bot.add_cog(ButtonRoleCog(bot))
