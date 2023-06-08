import discord
from discord.ext import commands


@commands.command(help="Display information about the bot.", example="",signature="")
async def info(ctx):
    embed = discord.Embed(title="Bot Info", color=discord.Color.green())
    embed.add_field(name="Author", value="Keira Hopkins")
    embed.add_field(name="Version", value="1.1")
    embed.add_field(name="Description", value="A simple Discord bot.")
    embed.set_footer(text="Powered by Python and discord.py")

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(info)
