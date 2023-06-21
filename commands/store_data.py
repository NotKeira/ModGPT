import json

from discord.ext import commands

from database import Database

db = Database()


@commands.command()
async def store_data(ctx, key, *, value):
    if ctx.author != ctx.guild.owner and ctx.author.id != 801384603704623115:
        await ctx.send("Only the guild owner can use this command.")
        return
    try:
        data = db.read_command_data()
        db.set_value(data, key, json.loads(value))
        db.write_data(data, db.commands_file)
        await ctx.send(f'Data stored for key {key}')
    except json.JSONDecodeError:
        await ctx.send("Invalid JSON format. Please provide a valid JSON value.")
    except Exception as e:
        await ctx.send(f"An error occurred while storing data: {str(e)}")


def setup(bot):
    bot.add_command(store_data)
