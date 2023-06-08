import discord
from discord.ext import commands
from database import CustomDatabase

db = CustomDatabase(guilds_file='guilds.json', users_file='users.json')

@commands.command(help="Retrieve data.", example="",signature="")
async def retrieve_data(ctx, option, key):
    if option.lower() == "user":
        data = db.read_user_data()
        user_id = str(ctx.author.id)
        if user_id not in data:
            await ctx.send("User data not found.")
            return
        data = data[user_id]
    elif option.lower() == "self":
        data = db.read_guild_data()
        if key.lower() == "self":
            guild_id = str(ctx.guild.id)
            if guild_id not in data:
                await ctx.send("Guild data not found.")
                return
            data = data[guild_id]
            key = guild_id
        else:
            guild_data = db.get_value(data, key)
            if guild_data is None:
                await ctx.send(f"No data found for self ID {key}.")
                return
            data = guild_data
    else:
        await ctx.send("Invalid option. Please choose either 'user' or 'self'.")
        return

    if isinstance(data, dict):
        embed = discord.Embed(title=f"Data for key: {key}", color=discord.Color.blue())
        for field_name, field_value in data.items():
            formatted_name = field_name.capitalize()
            embed.add_field(name=formatted_name, value=field_value, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"No data found for key {key}")


def setup(bot):
    bot.add_command(retrieve_data)
