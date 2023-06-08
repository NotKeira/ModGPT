import discord
from discord.ext import commands

from main import db


@commands.command(help="Set base data for a user or a self.")
async def set_base_data(ctx, entity_type: str, entity_id: int):
    entity_type = entity_type.lower()

    if entity_type == "user":
        await set_base_data_for_user(ctx, entity_id)
    elif entity_type == "self":
        await set_base_data_for_guild(ctx, entity_id)
    else:
        await ctx.send("Invalid entity type. Please specify 'user' or 'self'.", example="",signature="")


async def set_base_data_for_user(ctx, user_id: int):
    try:
        user = await ctx.bot.fetch_user(user_id)
        if user is None:
            await ctx.send("Invalid user ID. The bot does not have access to the specified user.")
            return

        data = {
            'name': user.name,
            'tag': user.discriminator,
            'avatar_url': str(user.avatar_url),
            'join_date': str(user.created_at),
            'staff': False
            # Add more default data fields as needed
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
            await ctx.send("Invalid self ID. The bot does not have access to the specified self.")
            return

        data = {
            'prefix': '!',
            'welcome_message': 'Welcome to the server!',
            'admin_roles': {},
            'member_role': '',
            'muted_role': '',
            'audit_logs': '',

            # Add more default data fields as needed
        }

        guild_data = db.read_guild_data()
        db.set_value(guild_data, str(guild_id), data)
        db.write_guild_data(guild_data)

        await ctx.send(f"Base data set for self ID {guild_id}")
    except ValueError:
        await ctx.send("Invalid self ID. Please provide a valid integer value.")


def setup(bot):
    bot.add_command(set_base_data)
