from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


def is_staff(ctx):
    user_id = str(ctx.author.id)
    user_data = Database().read_user_data()

    if user_id in user_data:
        user_info = user_data[user_id]
        staff = user_info.get("staff", False)
        return staff
    else:
        return False


@commands.command(help=command_data["staff"]["help"], example=command_data["staff"]["example"],
                  signature=command_data["staff"]["signature"])
async def staff(ctx, option: str):
    if is_staff(ctx):
        if option.lower() == "server_list":
            for guild in ctx.bot.guilds:
                await ctx.send(f"{guild.name} ({guild.id})")
        else:
            await ctx.send("No option chosen, however you are staff.")
    else:
        await ctx.send("This command can only be used by staff members.")


@staff.error
async def staff_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to use this command.")


def setup(bot):
    bot.add_command(staff)
