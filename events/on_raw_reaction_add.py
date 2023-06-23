from main import bot

message_id = 0  # Replace YOUR_MESSAGE_ID with the actual message ID
role_id = 0  # Replace YOUR_ROLE_ID with the actual role ID

async def on_raw_reaction_add(payload):
    if payload.message_id == message_id:  # Replace YOUR_MESSAGE_ID with the actual message ID
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Check if the reaction is from a bot or the role is already assigned
        if member.bot or role_id in [role.id for role in
                                     member.roles]:  # Replace YOUR_ROLE_ID with the actual role ID
            return

        # Check the emoji and assign the role accordingly
        if payload.emoji.name == "✅":
            role = guild.get_role(role_id)  # Replace YOUR_ROLE_ID with the actual role ID
            await member.add_roles(role)


def setup(bot):
    bot.add_listener(on_raw_reaction_add, 'on_raw_reaction_add')