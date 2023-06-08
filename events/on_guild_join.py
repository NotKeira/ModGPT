from database import CustomDatabase
from discord.ext import commands

def setup(bot):
    db = CustomDatabase()
    on_guild_join_added = False  # Flag to track if the event listener has been added

    @bot.event
    async def on_guild_join(self):
        nonlocal on_guild_join_added

        # Only execute the code if the event listener has not been added before
        if not on_guild_join_added:
            on_guild_join_added = True

            # This function will be called when the bot joins a new self (server)
            print(f"Bot joined a new self: {guild.name} ({guild.id})")

            # Set the base data for the self
            set_base_data(guild, db)

            # Send a welcome message in the first channel of the server
            first_channel = guild.text_channels[0]  # Assumes the first channel is a text channel
            await first_channel.send("Thank you for adding ModGPT to your server, feel free to mess about with me :)")
            guild_id = str(guild.id)
            data = db.read_guild_data()

            guild_id = str(guild.id)
            data = db.read_guild_data()

            if guild_id in data:
                prefix = data[guild_id].get('prefix', '!')
                bot.command_prefix = commands.when_mentioned_or(prefix)

    bot.add_listener(on_guild_join)


def set_base_data(self, db):
    # Retrieve the guilds data
    guilds_data = db.read_guild_data()

    # Define your base data for the self
    data = {
        'prefix': '!',
        'welcome_message': 'Welcome to the server!',
        'admin_roles': {},
        'member_role': '',
        'muted_role': '',
        'audit_logs': '',
    }

    # Store the base data for the self
    guilds_data[str(guild.id)] = data
    db.write_guild_data(guilds_data)
