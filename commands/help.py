from discord.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help_custom', example="",signature="")
    async def help_custom(self, ctx):
        # Help command logic
        await ctx.send('Custom help command')


def setup(bot):
    bot.add_cog(HelpCommand(bot))
