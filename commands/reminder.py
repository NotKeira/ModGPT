import asyncio
import math
import random
import time

import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["reminder"]["help"], example=command_data["reminder"]["example"],
                  signature=command_data["reminder"]["signature"])
async def reminder(ctx):
    current_time = math.ceil(time.time())
    reminder_time = ctx.message.content.split(" ")[1]
    reminder_reason = ' '.join(ctx.message.content.split(" ")[2:])
    index = random.randint(0, 99999999999999)
    data = {str(index): {"reason": reminder_reason, "time": 0, "author": ctx.message.author.id,
                         "channel": ctx.message.channel.id, "guild": ctx.message.guild.id,
                         "timestamp": math.ceil(current_time)}}

    if reminder_time.endswith("s"):
        reminder_time = int(reminder_time[:-1])
    elif reminder_time.endswith("m"):
        reminder_time = int(reminder_time[:-1]) * 60
    elif reminder_time.endswith("h"):
        reminder_time = int(reminder_time[:-1]) * 60 * 60
    elif reminder_time.endswith("d"):
        reminder_time = int(reminder_time[:-1]) * 60 * 60 * 24
    elif reminder_time.endswith("w"):
        reminder_time = int(reminder_time[:-1]) * 60 * 60 * 24 * 7
    elif reminder_time.endswith("mo"):
        reminder_time = int(reminder_time[:-1]) * 60 * 60 * 24 * 30
    elif reminder_time.endswith("y"):
        reminder_time = int(reminder_time[:-1]) * 60 * 60 * 24 * 365
    else:
        return await ctx.send("Invalid time format. Please use s, m, h, d, w, mo, or y.")

    data[str(index)]['time'] = math.ceil(current_time + reminder_time)
    await ctx.send(
        f"Reminder set for '{reminder_reason}' in <t:{data[str(index)]['time']}:R>. ||Debug Index: *{index}*||")
    db.add_reminder(data)

    # Calculate the time until the reminder triggers
    seconds_until_reminder = max(data[str(index)]['time'] - math.ceil(time.time()), 0)

    # Wait for the reminder duration
    await asyncio.sleep(seconds_until_reminder)

    # Send the reminder message
    reminder_embed = discord.Embed(title=f"Reminder for {reminder_reason}", color=0x07575b)
    reminder_embed.description = f"**Reminder set at**: <t:{data[str(index)]['timestamp']}:F>\n" \
                                 f"**Reminder set for**: <t:{data[str(index)]['time']}:F>"
    reminder_embed.set_footer(text=f"Reminder index: {index}")
    reply = await ctx.send(f"Hey <@{data[str(index)]['author']}> your reminder is done!", embed=reminder_embed)
    db.delete_reminder(str(index))  # Use str(index) instead of index
    message = await ctx.send(f"Reminder deleted. Index: {index}")
    await asyncio.sleep(3)
    await message.delete()


def setup(bot):
    bot.add_command(reminder)
