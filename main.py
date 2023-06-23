import inspect
import os
import sys
import traceback

import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import Database

load_dotenv()
bot_token = os.getenv('MODGPT_BOT_TOKEN')
bot = commands.Bot(command_prefix="r!", intents=discord.Intents.all(), help_command=None)
db = Database()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found.")
    elif isinstance(error, commands.MissingRequiredArgument):
        signature = inspect.signature(ctx.command.callback)
        missing_args = [param.name for param in signature.parameters.values() if
                        param.default == inspect.Parameter.empty]
        await ctx.send(f"Missing required argument(s): {', '.join(missing_args)}")
    else:
        await ctx.send(f"An error occurred: {error}")
        traceback.print_exc()


lst = []

# Load event files
print("Loading events...")
for filename in os.listdir('events'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'events.{filename[:-3]}')
        except Exception as e:
            print(f'Failed to load extension {filename[:-3]}.', file=sys.stderr)
            traceback.print_exc()
        else:
            lst += [filename[:-3]]

print(f'Loaded Events: {", ".join(lst)}')
lst = []


# Load command files
command_data = db.read_command_data()
print("Loading commands...")
for command in command_data:
    try:
        bot.load_extension(f'commands.{command}')
    except Exception as e:
        print(f'Failed to load extension {command}.', file=sys.stderr)
        traceback.print_exc()
    else:
        lst += [command]

print(f'Loaded Commands: {", ".join(lst)}')

bot.run(bot_token)

print(f'Loaded {len(lst)} commands.')
