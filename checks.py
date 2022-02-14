import disnake
from disnake.ext import commands

blacklisted_users = [
    # Start Blacklisted Users List
    # Enter USER_IDs separated by a comma.
    # Example:
    # 1234567890,
    # 1234567891,
]


def LEVEL_A(ctx):
    # Owner
    return (
        commands.has_role(847994265974997002)
        and ctx.message.author.id not in blacklisted_users
    )


def LEVEL_B(ctx):
    # Senior Administrator
    return (
        commands.has_role(846503865775030323)
        and ctx.message.author.id not in blacklisted_users
    )


def LEVEL_C(ctx):
    # Administrator
    return (
        commands.has_role(846502340017913907)
        and ctx.message.author.id not in blacklisted_users
    )


def LEVEL_L(ctx):
    # Head Moderator
    return commands.has_role() and ctx.message.author.id not in blacklisted_users


def LEVEL_M(ctx):
    # Moderator
    return commands.has_role() and ctx.message.author.id not in blacklisted_users


def LEVEL_N(ctx):
    # Junior Moderator
    return commands.has_role() and ctx.message.author.id not in blacklisted_users


def LEVEL_W(ctx):
    # Regular Member
    return (
        commands.has_role(845457100582420510)
        and ctx.message.author.id not in blacklisted_users
    )
