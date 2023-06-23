import math
import random
import time

import discord
from discord.ext import commands

from database import Database

db = Database()
command_data = db.read_command_data()
infraction_data = db.get_infractions()


@commands.command(help=command_data["warn"]["help"], example=command_data["warn"]["example"],
                  signature=command_data["warn"]["signature"])
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member: discord.Member, *, reason: str):
    current_time = math.ceil(time.time())
    identifier = f"{random.randint(0, 9999999999999)}_{member.id}"
    data = {str(identifier): {"type": "warn", "reason": reason, "user_id": member.id, "moderator": ctx.author.id,
                              "guild": ctx.guild.id, "timestamp": math.ceil(current_time)}}

    run = db.add_infraction(data, identifier)
    if run is False:
        await ctx.send("An error occurred while adding the infraction to the database.")
        return
    else:
        embed = discord.Embed(title=f"Warned {member.name}", description=f"Reason: {reason}", color=0x00ff00)
        await ctx.send(embed=embed)

        await member.send(embed=discord.Embed(title=f"You have been warned in {ctx.guild.name}",
                                              description=f"Reason: {reason}", color=0xFF9999))
        await member.send(f"**Infraction ID:** {identifier}")

        await publish_infraction(ctx, member, reason, identifier, "warn")


async def publish_infraction(ctx, member, reason, identifier, type):
    channel = ctx.guild.get_channel(1121070010526351370)
    embed = discord.Embed(title=f"{type.capitalize()} Issued", color=0xFF9999)
    embed.description = f"**Reason:** {reason}" \
                        f"\n**Infraction ID:** {identifier}" \
                        f"\n**Member:** {member.mention}" \
                        f"\n**Moderator:** {ctx.author.mention}"
    embed.timestamp = ctx.message.created_at
    await channel.send(embed=embed)


def setup(bot):
    bot.add_command(warn)
