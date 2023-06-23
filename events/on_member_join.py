from database import Database
from main import bot

db = Database()


async def handle_member_join(member):
    guild_id = str(member.guild.id)
    data = db.read_guild_data()

    if guild_id in data:
        guild_config = data[guild_id]
        channel = bot.get_channel(guild_config.get("welcome_channel"))
        await channel.send(f'{member.name} has joined the server.')
    else:
        print("Guild not found in database, cannot send welcome message.")
    message = f'Welcome to {member.guild.name}!' \
              f'Please read the rules in {member.guild.get_channel(997822977431318540).mention} ' \
              f'and assign yourself a role in {member.guild.get_channel(1120695212071735336).mention}!' \
              f'If you have any questions, feel free to ask in {member.guild.get_channel(1120695363033112646).mention}!' \
              f'If you would like to see a list of commands, type `r!help` in {member.guild.get_channel(997849339454038077).mention}!' \

    sent = await member.send(message)
    await sent.add_reaction('<:diamond:1024029867651633202>')
    await member.add_roles(member.guild.get_role(997823052521930822))


def setup(bot):
    bot.add_listener(handle_member_join, 'on_member_join')
