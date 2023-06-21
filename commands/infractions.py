from discord import Embed
from discord import Member as DiscordMember
from discord.ext import commands

from database import Database

db = Database()


@commands.command()
async def infractions(ctx, member: DiscordMember):
    infractions = db.get_infractions()
    member_infractions = []

    for infraction_type in infractions:
        for infraction_id, infraction_data in infractions[infraction_type].items():
            if infraction_data['user_id'] == member.id:
                member_infractions.append((infraction_id, infraction_data))

    if len(member_infractions) == 0:
        await ctx.send(f"{member.mention} has no infractions.")
    else:
        await ctx.send(f"{member.mention} has {len(member_infractions)} infractions.")
        embed = Embed(title=f"Infractions for {member.name}", color=0xFF9999)

        for infraction_id, infraction_data in member_infractions:
            embed.add_field(name=f"Infraction ID: {infraction_id}", value=f"Type: {infraction_data['type']}\n"
                                                                          f"Reason: {infraction_data['reason']}\n"
                                                                          f"Timestamp: {infraction_data['timestamp']}\n"
                                                                          f"Moderator: <@{infraction_data['moderator']}>")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(infractions)
