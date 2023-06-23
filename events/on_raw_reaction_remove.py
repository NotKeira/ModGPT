from database import Database
from main import bot

db = Database()


async def on_raw_reaction_remove(payload):
    message_id = str(payload.message_id)
    role_id = 0

    if payload.message_id == message_id:  # Replace YOUR_MESSAGE_ID with the actual message ID
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        # Check if the role is already removed or the reaction is from a bot
        if member.bot or role_id not in [role.id for role in
                                              member.roles]:  # Replace YOUR_ROLE_ID with the actual role ID
            return

        # Check the emoji and remove the role accordingly
        if payload.emoji.name == "✅":
            role = guild.get_role(role_id)  # Replace YOUR_ROLE_ID with the actual role ID
            await member.remove_roles(role, reason="User removed reaction")


def setup(bot):
    bot.add_listener(on_raw_reaction_remove, "on_raw_reaction_remove")
