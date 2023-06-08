async def handle_member_join(member):
    channel = bot.get_channel(1099456169656979629)  # Replace with your desired channel ID
    await channel.send(f'{member.name} has joined the server.')

def setup(bot):
    bot.add_listener(handle_member_join, 'on_member_join')
