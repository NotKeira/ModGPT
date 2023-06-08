from discord.ext import commands

@commands.command(help="Say hello", example="",signature="")
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

def setup(bot):
    bot.add_command(hello)
