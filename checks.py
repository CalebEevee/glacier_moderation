import disnake
from disnake.ext import commands

blacklisted_users = []


def LEVEL_A(ctx):
    return (
        commands.has_role(847994265974997002)
        and ctx.message.author.id not in blacklisted_users
    )


def LEVEL_W(ctx):
    return (
        commands.has_role(845457100582420510)
        and ctx.message.author.id not in blacklisted_users
    )
