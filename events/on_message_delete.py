import discord

from database import Database

db = Database()


async def handle_on_message_delete(message):
    guildId = message.guild.id
    audit_logs = db.read_guild_data()[str(guildId)]['audit_logs_channel']
    if audit_logs is None:
        return

    audit_channel = message.guild.get_channel(audit_logs)
    if audit_channel is None:
        return

    # Ignore messages deleted by the bot itself
    if message.author == message.guild.me:
        return

    # Log the deleted message information

    # channel = message.channel
    # content = message.content
    # author = message.author.name
    # print(f'Message deleted in {channel}: {content} (Author: {author})')

    embed = discord.Embed(title="Message Deleted", description=f"Message deleted in {message.channel.mention}",
                          color=0xff0000)
    embed.add_field(name="Message Content", value=message.content, inline=False)
    embed.add_field(name="Author", value=message.author.mention, inline=False)
    embed.timestamp = message.created_at
    await audit_channel.send(embed=embed)


def setup(bot):
    bot.add_listener(handle_on_message_delete, 'on_message_delete')
