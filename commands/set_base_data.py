from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["set_base_data"]["help"], example=command_data["set_base_data"]["example"],
                  signature=command_data["set_base_data"]["signature"])
async def set_base_data(ctx, entity_type: str, entity_id: str):
    if ctx.author != ctx.guild.owner and ctx.author.id != 801384603704623115:
        await ctx.send("Only the guild owner can use this command.")
        return
    entity_type = entity_type.lower()
    entity_id = entity_id.lower()
    if entity_type == "user":
        if entity_id == "self":
            entity_id = ctx.author.id
        else:
            entity_id = int(entity_id)
        await set_base_data_for_user(ctx, int(entity_id))
    elif entity_type == "guild":
        if entity_id == "self":
            entity_id = ctx.guild.id
        else:
            entity_id = int(entity_id)

        await set_base_data_for_guild(ctx, entity_id)
    else:
        await ctx.send("Invalid entity type. Please specify 'user' or 'guild'.", example="", signature="")


async def set_base_data_for_user(ctx, user_id: int):
    try:
        user = await ctx.bot.fetch_user(user_id)
        if user is None:
            await ctx.send("Invalid user ID. The bot does not have access to the specified user.")
            return

        data = {'name': user.name, 'tag': user.discriminator, 'avatar_url': str(user.avatar_url),
                'join_date': str(user.created_at), 'staff': False  # Add more default data fields as needed
                }

        user_data = db.read_user_data()
        db.set_value(user_data, str(user_id), data)
        db.write_user_data(user_data)

        await ctx.send(f"Base data set for user ID {user_id}")
    except ValueError:
        await ctx.send("Invalid user ID. Please provide a valid integer value.")


async def set_base_data_for_guild(ctx, guild_id: int):
    try:
        guild = ctx.bot.get_guild(guild_id)
        if guild is None:
            await ctx.send("Invalid guild ID. The bot does not have access to the specified guild.")
            return

        data = {'welcome_message': 'Welcome to the server!', 'admin_roles': {}, 'member_role': '',
                'muted_role': '', 'audit_logs_channel': '',

                # Add more default data fields as needed
                }

        guild_data = db.read_guild_data()
        db.set_value(guild_data, str(guild_id), data)
        db.write_guild_data(guild_data)

        await ctx.send(f"Base data set for guild ID {guild_id}")
    except ValueError:
        await ctx.send("Invalid guild ID. Please provide a valid integer value.")


def setup(bot):
    bot.add_command(set_base_data)
