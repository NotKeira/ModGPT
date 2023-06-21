from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["ping"]["help"], example=command_data["ping"]["example"],
                  signature=command_data["ping"]["signature"])
async def ping(ctx):
    latency = round(ctx.bot.latency * 1000)  # Multiply by 1000 to get latency in milliseconds
    await ctx.send(f"Pong! Latency: {latency}ms")


def setup(bot):
    bot.add_command(ping)
