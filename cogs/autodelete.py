import disnake
from disnake.ext import commands

import checks
import classes


class AutoDelete(commands.Cog):
    """Advertisement autodeleter."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        channels = [
            846518605751386153,
            846518677686845450,
            846518922798039040,
            846529278614175786,
            846519205700435989,
            846530118558285844,
            846528045678329866,
            846527744691273768,
            846519113156526111,
            846527296193822730,
            846528975526166528,
            846527906004205569,
            846526019157360650,
            847247183296069702,
            847254098142167050,
            847254177557774386,
            847253712439214110,
            847255699662307348,
            847255510364979240,
            853337250267922492,
            853337373630267442,
            853337722198032394,
            846527379202768896,
        ]

        def check(m):
            return m.author == member

        logchannel = self.bot.get_channel(926546479718498344)

        for channel_id in channels:
            channel = await self.bot.get_channel(channel_id)
            deleted = await channel.purge(limit=100, check=check)

        embed = disnake.Embed(
            title="AutoDelete - Member Left",
            description=f"{member.name} `[ {member.id} ]` left. {len(deleted)} message(s) deleted!",
            color=0x56C9F0,
        )

        await logchannel.send(embed=embed)


def setup(bot):
    bot.add_cog(AutoDelete(bot))
