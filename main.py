import inspect
import os

from discord.ext import commands
from dotenv import load_dotenv

from database import CustomDatabase

load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
bot = commands.Bot(command_prefix='!')
db = CustomDatabase(guilds_file='guilds.json', users_file='users.json')


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


# Load event files
for filename in os.listdir('events'):
    if filename.endswith('.py'):
        bot.load_extension(f'events.{filename[:-3]}')

# Load command files
for filename in os.listdir('commands'):
    if filename.endswith('.py'):
        bot.load_extension(f'commands.{filename[:-3]}')

bot.run(bot_token)
