import math
import random
import time

import discord
from discord.ext import commands

from database import Database

db = Database()
command_data = db.read_command_data()


@commands.command(help=command_data["ban"]["help"], example=command_data["ban"]["example"],
                  signature=command_data["ban"]["signature"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        reason = 'No reason provided'
    else:
        pass
    if member == ctx.author:
        await ctx.send('You cannot ban yourself!')
        return
    if member == ctx.guild.owner:
        await ctx.send('You cannot ban the owner!')
        return
    if member.top_role >= ctx.author.top_role:
        await ctx.send('You cannot ban someone with a higher role than you!')
        return
    if member.top_role >= ctx.guild.me.top_role:
        await ctx.send('I cannot ban someone with a higher role than me!')
        return
    if member == ctx.guild.me:
        await ctx.send('I cannot ban myself!')
        return
    await member.send(f'You have been banned from {ctx.guild.name} for {reason}.')
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member} for `{reason}`.')

    current_time = math.ceil(time.time())
    identifier = f"{random.randint(0, 9999999999999)}_{member.id}"
    data = {str(identifier): {"type": "ban", "reason": reason, "user_id": member.id, "moderator": ctx.author.id,
                              "guild": ctx.guild.id, "timestamp": math.ceil(current_time)}}

    db.add_infraction(data, identifier)
    data = db.read_guild_data()
    guild_data = data[str(ctx.guild.id)]
    if guild_data is None:
        return
    if guild_data['staff_logs_channel'] is None:
        print('No staff logs channel set.')
        return
    else:
        channel = ctx.guild.get_channel(data['staff_logs_channel'])
        if channel is None:
            print('Invalid staff logs channel.')
            return
        else:
            embed = discord.Embed(title='Ban',
                                  description=f'**User:** {member}\n**Moderator:** {ctx.author}\n**Reason:** {reason}',
                                  color=discord.Color.red())
            embed.timestamp = ctx.message.created_at
            await channel.send(embed=embed)



def setup(bot):
    bot.add_command(ban)
