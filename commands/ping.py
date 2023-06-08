from discord.ext import commands


def setup(bot):
    @commands.command(help="Check the bots latency.", example="",signature="")
    async def ping(ctx):
        latency = round(bot.latency * 1000)  # Multiply by 1000 to get latency in milliseconds
        await ctx.send(f"Pong! Latency: {latency}ms")

    bot.add_command(ping)
