from discord.ext import commands
import json
from main import db


@commands.command(help="Store self.", example="",signature="")
async def store_data(ctx, key, *, value):
    try:
        data = db.read_data()
        db.set_value(data, key, json.loads(value))
        db.write_data(data)
        await ctx.send(f'Data stored for key {key}')
    except json.JSONDecodeError:
        await ctx.send("Invalid JSON format. Please provide a valid JSON value.")
    except Exception as e:
        await ctx.send(f"An error occurred while storing self: {str(e)}")


def setup(bot):
    bot.add_command(store_data)
