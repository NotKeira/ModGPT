from database import Database
from main import bot

db = Database()


async def handle_member_remove(member):
    guild_id = str(member.guild.id)
    data = db.read_guild_data()
    usage_data = db.get_usage()

    if guild_id in data:
        guild_config = data[guild_id]
        channel = bot.get_channel(guild_config.get("welcome_channel"))
        await channel.send(f'{member.name} has left the server.')
    else:
        print("Guild not found in database, cannot send welcome message.")


def setup(bot):
    bot.add_listener(handle_member_remove, 'on_member_remove')
