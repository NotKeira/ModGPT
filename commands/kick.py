import discord
from discord.ext import commands


@commands.command(help="Kick a member", example="",signature="")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f'{member.name} has been kicked!')


def setup(bot):
    bot.add_command(kick)
