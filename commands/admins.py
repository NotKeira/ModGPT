import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["admins"]["help"], example=command_data["admins"]["example"],
                  signature=command_data["admins"]["signature"])
async def admins(ctx):
    guild_id = str(ctx.guild.id)

    guild_data = db.read_guild_data()

    if guild_id not in guild_data:
        await ctx.send("Guild data not found.")
        return

    data = guild_data[guild_id]
    roles = data.get("admin_roles", {})

    if not roles:
        await ctx.send("No roles found in the guild data.")
        return

    admin_roles = [role_id for role_id, role_info in roles.items() if role_info.get("admin", False)]

    if not admin_roles:
        await ctx.send("No admins found in the guild data.")
        return

    embed = discord.Embed(title="Admins in this Guild", color=discord.Color.blue())
    for idx, admin_role_id in enumerate(admin_roles, 1):
        role = ctx.guild.get_role(int(admin_role_id))
        if role:
            admin_members = [member for member in ctx.guild.members if role in member.roles]
            if admin_members:
                members_list = "\n".join([f"<@!{member.id}> - {member.id}" for member in admin_members])
                embed.add_field(name=f"Admin #{idx} ({role.name})", value=members_list, inline=False)
            else:
                embed.add_field(name=f"Admin #{idx} ({role.name})", value="*No members with this role*", inline=False)

    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(admins)
