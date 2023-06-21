from discord.ext import commands
from database import Database
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["config"]["help"], example=command_data["config"]["example"],
                  signature=command_data["config"]["signature"])
async def config(ctx, variable, value):
    if ctx.author != ctx.guild.owner and ctx.author.id != 801384603704623115:
        await ctx.send("Only the guild owner can use this command.")
        return
    guild_id = str(ctx.guild.id)  # Convert self ID to string
    data = db.read_guild_data()

    if guild_id in data:
        guild_config = data[guild_id]
        if variable == "admin_roles":
            # Convert the value to a dictionary with "admin": True for each role
            roles = [role.strip() for role in value.split(",")]
            admin_roles = {role: {"admin": True} for role in roles}
            guild_config[variable] = admin_roles
        else:
            guild_config[variable] = value

        db.write_guild_data(data)
        await ctx.send(f"Updated {variable} to {value} for this self.")
    else:
        await ctx.send("Guild configuration data not found.")


def setup(bot):
    bot.add_command(config)
