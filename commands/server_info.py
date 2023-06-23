import discord
from discord.ext import commands
from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["server_info"]["help"], example=command_data["server_info"]["example"],
                  signature=command_data["server_info"]["signature"])
async def server_info(ctx):
    server = ctx.guild
    total_members = server.member_count
    online_members = len([m for m in server.members if m.status != discord.Status.offline])
    text_channels = len(server.text_channels)
    voice_channels = len(server.voice_channels)
    categories = len(server.categories)

    embed = discord.Embed(title=f"{server.name} Server Info", color=discord.Color.blue())
    embed.description = (
        f"**Total Members:** {total_members}\n"
        f"**Online Members:** {online_members}\n"
        f"**Text Channels:** {text_channels}\n"
        f"**Voice Channels:** {voice_channels}\n"
        f"**Categories:** {categories}"
    )

    await ctx.send(embed=embed)


@server_info.error
async def server_info_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Failed to retrieve server information.")
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command cannot be used in private messages.")
    else:
        await ctx.send("An error occurred while executing the command.")


def setup(bot):
    bot.add_command(server_info)
