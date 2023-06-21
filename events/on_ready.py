from database import Database
from main import bot
from os import getenv
db = Database()


async def handle_on_ready():
    print('Bot is ready!')
    if getenv('MAINTENANCE') == 'True':
        print('MAINTENANCE MODE ENABLED')
    else:
        print('MAINTENANCE MODE DISABLED')
        try:
            channel_id = 997827352534978602
            channel = bot.get_channel(channel_id)
            if channel is not None:
                # Channel found, proceed with your code
                print(f"Channel with ID {channel_id} found.")
                await channel.send("Bot is ready!")
            else:
                # Channel not found, handle the error
                print(f"Error: Channel with ID {channel_id} not found or inaccessible.")

        except Exception as e:
            print(e)
            print("Failed to send message to channel")


def setup(bot):
    bot.add_listener(handle_on_ready, 'on_ready')
