import discord
from discord.ext import commands

from database import CustomDatabase as db


class CommandLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def create_audit_logs_channel(self):
        overwrites = {self.default_role: discord.PermissionOverwrite(read_messages=False),
                      self.me: discord.PermissionOverwrite(read_messages=True)}
        return await self.create_text_channel("audit_logs", overwrites=overwrites)

    async def get_audit_logs_channel(self):
        audit_logs_channel = discord.utils.get(self.text_channels, name="audit_logs")
        if audit_logs_channel is None:
            audit_logs_channel = discord.utils.get(self.text_channels, name="audit-logs")
        return audit_logs_channel

    @commands.Cog.listener()
    async def on_command(self, ctx):
        guild_id = str(ctx.guild.id)
        data = db.read_guild_data()

        if guild_id in data:
            guild_config = data[guild_id]
            audit_logs_channel_id = guild_config.get("audit_logs")

            if audit_logs_channel_id:
                channel = self.bot.get_channel(int(audit_logs_channel_id))
            else:
                guild = ctx.guild
                channel = await self.get_audit_logs_channel(guild)
                if channel is None:
                    channel = await self.create_audit_logs_channel(guild)
                guild_config["audit_logs"] = channel.id
                db.write_guild_data(data)

            if channel is not None:
                log_message = f"Command `{ctx.message.content}` run by {ctx.author} in <#{ctx.channel.id}>"
                await channel.send(log_message)


def setup(bot):
    bot.add_cog(CommandLogger(bot))
