import discord
from discord.ext import commands

from database import Database

db = Database()


@commands.command()
async def announce(ctx, *, message):
    if ctx.author.guild_permissions.administrator:
        await ctx.message.delete()
        embed = discord.Embed(description=message, color=discord.Color.blue())
        embed.timestamp = ctx.message.created_at
        await ctx.send(embed=embed)
    else:
        await ctx.send("You do not have permission to use this command.")
