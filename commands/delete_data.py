from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["cmd_info"]["help"], example=command_data["cmd_info"]["example"],
                  signature=command_data["cmd_info"]["signature"])
async def delete_data(self, ctx,path, key):
    if ctx.author.id != 801384603704623115:
        await ctx.send("Only Rune or ModGPT Staff can use this command.")
        return
    else:
        data = db.read_data(file_path=path)

        db.delete_value(data, key)
        db.write_data(data,file_path=path)
        new_data = db.read_data(file_path=path)
        await ctx.send(f'Data deleted for key {key}')
        await ctx.send(f'New data: {new_data}')
        print(f'Data deleted for key {key}')


def setup(bot):
    bot.add_command(bot)
