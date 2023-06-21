import discord
from discord.ext import commands
from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["whois"]["help"], example=command_data["whois"]["example"],
                  signature=command_data["whois"]["signature"])
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(title="User Info", color=member.color)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="Username", value=member.name)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Status", value=member.status)
    embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    embed.add_field(name="Roles", value=',\n '.join([role.name for role in member.roles[1:]]))

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(whois)
