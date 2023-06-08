from discord.ext import commands
from database import CustomDatabase


def is_staff(ctx):
    user_id = str(ctx.author.id)
    user_data = CustomDatabase().read_user_data()

    if user_id in user_data:
        user_info = user_data[user_id]
        staff = user_info.get("staff", False)
        return staff
    else:
        return False


@commands.command(help="This is a staff-only command.")
async def staff_command(ctx):
    if is_staff(ctx):
        await ctx.send("You're staff!")
    else:
        await ctx.send("This command can only be used by staff members.")


@staff_command.error
async def staff_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to use this command.")


def setup(bot):
    bot.add_command(staff_command)
