import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["reminders"]["help"], example=command_data["reminders"]["example"],
                  signature=command_data["reminders"]["signature"])
async def reminders(ctx):
    reminders_data = db.get_reminders()
    guild_reminders = [reminder_data for reminder_data in reminders_data.values() if
                       int(reminder_data.get("guild")) == ctx.guild.id]

    if not guild_reminders:
        await ctx.send("No reminders in this guild.")
        return

    embed = discord.Embed(title=f"Reminders for {ctx.guild.name}", color=0x00ff00)

    for reminder_data in guild_reminders:
        reminder_reason = reminder_data.get("reason")
        reminder_time = reminder_data.get("time")
        embed.add_field(name=f"Reminder for {reminder_reason}",
                        value=f"Set for <t:{reminder_time}:R> (<t:{reminder_time}:F>).", inline=False)

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(reminders)
