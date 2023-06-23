import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["info"]["help"], example=command_data["info"]["example"],
                  signature=command_data["info"]["signature"])
async def info(ctx):
    embed = discord.Embed(title="Bot Info", color=discord.Color.green())
    embed.add_field(name="Author", value="Keira Hopkins")
    embed.add_field(name="Version", value="1.1")
    embed.add_field(name="Description", value="A simple Discord bot.")
    embed.set_footer(text="Powered by Python and discord.py")

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(info)
