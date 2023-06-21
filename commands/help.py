import discord
from discord.ext import commands

from database import Database

db = Database()


@commands.command()
async def help(ctx, command_name=None):
    command_data = db.read_command_data()
    if command_name is None or command_name.lower() == "all":
        bot = ctx.bot
        embed = discord.Embed(title="Available Commands", color=discord.Color.purple())
        for command_name, command_info in command_data.items():
            command_name_1 = command_name.replace("_", " ").title()
            description = command_info.get("help", "No description provided.")
            embed.add_field(name=str(command_name_1 + " (" + command_name + ")"), value=description, inline=False)
        await ctx.send(embed=embed)
    else:
        if command_name in command_data:
            command_info = command_data[command_name]
            embed = discord.Embed(title=f"Command Info: {command_name}", color=discord.Color.blue())
            embed.description = f"**Description:** {command_info.get('help', 'No description provided')}\n"
            embed.description += f"**Signature:** {command_info.get('signature', 'No signature provided')}\n"
            custom_example = command_info.get('example')
            if custom_example:
                embed.description += f"**Custom Example:** {custom_example}"
            await ctx.send(embed=embed)
        else:
            await ctx.send("Command not found.")


def setup(bot):
    bot.add_command(help)
