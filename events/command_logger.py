import random

import discord
from discord.ext import commands

from database import Database

db = Database()


class CommandLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_role = None
        self.me = None

    @staticmethod
    async def create_audit_logs_channel(guild):
        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False),
                      guild.me: discord.PermissionOverwrite(read_messages=True)}
        return await guild.create_text_channel("audit_logs", overwrites=overwrites)

    @staticmethod
    async def get_audit_logs_channel(guild):
        audit_logs_channel = discord.utils.get(guild.text_channels, name="audit_logs")
        if audit_logs_channel is None:
            audit_logs_channel = discord.utils.get(guild.text_channels, name="audit-logs")
        return audit_logs_channel

    @commands.Cog.listener()
    async def on_command(self, ctx):
        guild_id = str(ctx.guild.id)
        data = db.read_guild_data()
        usage_data = db.get_usage()

        if guild_id in data:
            guild_config = data[guild_id]
            audit_logs_channel_id = guild_config.get("audit_logs_channel")

            if audit_logs_channel_id:
                channel = self.bot.get_channel(int(audit_logs_channel_id))
            else:
                guild = ctx.guild
                channel = await self.get_audit_logs_channel(guild)
                if channel is None:
                    channel = await self.create_audit_logs_channel(guild)
                guild_config["audit_logs_channel"] = channel.id
                db.write_guild_data(data)

            if channel is not None:
                log_message = f"Command `{ctx.message.content}` run by {ctx.author} in <#{ctx.channel.id}>"
                await channel.send(log_message)

                command_data = {"name": ctx.command.name, "user_id": str(ctx.author.id),
                                "command_id": f"{ctx.command.name}_{generate_random_integer()}",
                                "command_usage": ctx.message.content, "guild": str(ctx.guild.id),
                                "channel": str(ctx.channel.id)}

                usage_data[command_data["command_id"]] = command_data
                db.add_usage(usage_data)
                #print_data(command_data)


def setup(bot):
    bot.add_cog(CommandLogger(bot))


def generate_random_integer():
    return str(random.randint(1, 999999999999999))


def print_data(data):
    capitalized_command_data = {}

    for key, value in data.items():
        capitalized_key = ' '.join([x.capitalize() for x in key.split("_")])
        capitalized_command_data[capitalized_key] = value

    for key, value in capitalized_command_data.items():
        print(key + ":", value)
