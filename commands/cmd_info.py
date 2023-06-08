import discord
from discord.ext import commands


def setup(bot):
    @commands.command(help="Get information about a specific command.", example="",signature="")
    async def cmd_info(ctx, command_name):
        command = bot.get_command(command_name)

        if command:
            embed = discord.Embed(title=f"Command Info: {command.name}", color=discord.Color.blue())
            embed.add_field(name="Description", value=command.help or "No description provided.")
            embed.add_field(name="Usage", value=f"```{ctx.prefix}{command.name} {command.signature}```")
            embed.add_field(name="Example", value=f"```{ctx.prefix}{command.name} {command.example}```")

            await ctx.send(embed=embed)
        else:
            await ctx.send("Command not found.")

    bot.add_command(cmd_info)
