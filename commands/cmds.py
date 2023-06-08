import os

import discord
from discord.ext import commands


@commands.command(help="Display available commands.", example="",signature="")
async def cmds(ctx):
    bot = ctx.bot  # Get the bot instance from the context

    embed = discord.Embed(title="Available Commands", color=discord.Color.purple())

    # Loop through each command file in the "commands" directory
    for filename in os.listdir('commands'):
        if filename.endswith('.py'):
            command_name = filename[:-3]  # Get the command name by removing the .py extension
            command_module = f'commands.{command_name}'
            command = bot.get_command(command_name)

            if command:
                description = command.help or "No description provided."
                embed.add_field(name=command_name, value=description, inline=False)

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(cmds)
