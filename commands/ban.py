import discord
from discord.ext import commands


@commands.command(help=command_data["admins"]["help"], example=command_data["admins"]["example"],
                  signature=command_data["admins"]["signature"]))
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.name} has been banned.")


def setup(bot):
    bot.add_command(ban)
