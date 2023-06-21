import math
import random
import time

import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["kick"]["help"], example=command_data["kick"]["example"],
                  signature=command_data["kick"]["signature"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = 'No reason provided'
    else:
        pass
    if member == ctx.author:
        await ctx.send('You cannot kick yourself!')
        return
    if member == ctx.guild.owner:
        await ctx.send('You cannot kick the owner!')
        return
    if member.top_role >= ctx.author.top_role:
        await ctx.send('You cannot kick someone with a higher role than you!')
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send('I cannot kick someone with a higher role than me!')
        return
    if member == ctx.guild.me:
        await ctx.send('I cannot kick myself!')
        return

    await member.send(f'You have been kicked from {ctx.guild.name} for {reason}.')
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member} for `{reason}`.')
    current_time = math.ceil(time.time())
    identifier = f"{random.randint(0, 9999999999999)}_{member.id}"
    data = {str(identifier): {"type": "kick", "reason": reason, "user_id": member.id, "moderator": ctx.author.id,
                              "guild": ctx.guild.id, "timestamp": math.ceil(current_time)}}

    db.add_infraction(data, identifier)
    return


def setup(bot):
    bot.add_command(kick)
