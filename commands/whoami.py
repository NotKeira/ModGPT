import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["whoami"]["help"], example=command_data["whoami"]["example"],
                  signature=command_data["whoami"]["signature"])
async def whoami(ctx):
    embed = discord.Embed(title="Information", color=0xFF9999)
    embed.description = "Hello, so you're curious who I am? Well, I'm glad you asked!\n\n" \
                        "**Who Is <@1121061482197688340>?**\n" \
                        "This bot is used to moderate and protect the members of Sunrise."
    embed.add_field(name="What Can I Do?", value="I can do a lot of things, but here are some of my main features:\n"
                                                 "- Moderation\n"
                                                 "- Verification\n"
                                                 "- Auto-Role\n"
                                                 "- Auto-Mod\n"
                                                 "- Support Tickets\n"
                                                 "- Suggestions\n"
                                                 "- Reminders\n"
                                                 "- Logging\n"
                                                 "- Fun Commands\n"
                                                 "- And More!")
    embed.add_field(name="How Do I Use This Bot?", value="You can use this bot by typing `m!help` to see a list of "
                                                         "commands. You can also type `m!help <command>` to see "
                                                         "more information about a specific command.")
    embed.set_footer(
        text="If you have any questions, please contact us by sending 'I need help with the bot' to this bot.")
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(whoami)
