import discord

from database import Database

db = Database()


async def handle_on_message_edit(before, after):
    if before.content != after.content:
        # Log the edited message details to a file
        guildId = before.guild.id
        audit_logs = db.read_guild_data()[str(guildId)]['audit_logs_channel']
        if audit_logs is None:
            return
        else:
            embed = discord.Embed(title="Message Edited", description=f"Message edited in {before.channel.mention}",
                                  color=0xD8B8C8)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.add_field(name="Author", value=before.author.mention, inline=False)
            embed.timestamp = before.created_at
            auditChannel = before.guild.get_channel(audit_logs)
            await auditChannel.send(embed=embed)


def setup(bot):
    bot.add_listener(handle_on_message_edit, 'on_message_edit')
