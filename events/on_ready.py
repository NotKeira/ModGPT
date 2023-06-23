from os import getenv

import discord

from database import Database
from main import bot

db = Database()


async def handle_on_ready():
    print('Bot is ready!')
    if getenv('MAINTENANCE') == 'True':
        print('MAINTENANCE MODE ENABLED')
    else:
        print('MAINTENANCE MODE DISABLED')
        try:
            channel_id = 774943350537191444
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


 # # await send_update_message(bot)
async def send_update_message(bot):
    new_prefix = "r!"

    for guild in bot.guilds:
        channels = guild.text_channels
        first_channel = channels[0] if channels else None

        if first_channel:
            message = f"Hello everyone! I have some exciting news to share.\n\n" \
                      f"I have been upgraded with new and improved code. As a result, there are some changes:\n" \
                      f"- The prefix has been updated to `{new_prefix}`\n" \
                      f"- Various bug fixes and enhancements\n\n" \
                      f"Please feel free to ask any questions you may have. Thank you for your continued support!"

            try:
                await first_channel.send(message)
                print(f"Update message sent in the first channel of {guild.name}")
            except discord.Forbidden:
                print(f"Unable to send update message in the first channel of {guild.name} (permission error)")
            except discord.HTTPException:
                print(f"Unable to send update message in the first channel of {guild.name} (HTTP exception)")
        else:
            print(f"No text channels found in {guild.name}")



def setup(bot):
    bot.add_listener(handle_on_ready, 'on_ready')
