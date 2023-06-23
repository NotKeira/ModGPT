from database import Database


def setup(bot):
    db = Database()
    on_guild_join_added = False  # Flag to track if the event listener has been added

    @bot.event
    async def on_guild_join(self, guild):
        nonlocal on_guild_join_added

        # Only execute the code if the event listener has not been added before
        if not on_guild_join_added:
            on_guild_join_added = True

            print(f"Joined guild '{guild.name}' (ID: {guild.id}). Default prefix set to 'r!'.")
            # This function will be called when the bot joins a new self (server)
            print(f"Bot joined a new guild: {guild.name} ({guild.id})")

            # Set the base data for the self
            set_base_data(guild, db)

            # Send a welcome message in the first channel of the server
            first_channel = guild.text_channels[0]  # Assumes the first channel is a text channel
            await first_channel.send("Thank you for adding ModGPT to your server, feel free to mess about with me :)")
        else:
            # This is a guild that the bot has already joined
            print(f"Bot rejoined a guild: {guild.name} ({guild.id})")

    bot.add_listener(on_guild_join)


def set_base_data(guild, db):
    # Retrieve the guilds data
    guilds_data = db.read_guild_data()

    # Define your base data for the self
    data = {'prefix': 'r!', 'welcome_message': 'Welcome to the server!', 'admin_roles': {}, 'member_role': '',
        'muted_role': '', 'audit_logs': '', }

    # Store the base data for the self
    guilds_data[str(guild.id)] = data
    db.write_guild_data(guilds_data)
