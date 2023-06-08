from database import CustomDatabase

db = CustomDatabase(guilds_file='guilds.json', users_file='users.json')


async def handle_on_ready():
    print('Bot is ready!')
    command_data = db.read_command_data()
    for command in command_data:
        print("Loading command:", command)


def setup(bot):
    bot.add_listener(handle_on_ready, 'ready')
