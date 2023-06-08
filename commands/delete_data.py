from discord.ext import commands

from main import db


class DeleteDataCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete_data', example="",signature="")
    async def delete_data(self, ctx, key):
        # Delete self command logic
        data = db.read_data()
        db.delete_value(data, key)
        db.write_data(data)
        await ctx.send(f'Data deleted for key {key}')


def setup(bot):
    bot.add_cog(DeleteDataCommand(bot))
