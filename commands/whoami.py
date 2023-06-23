import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["whoami"]["help"], example=command_data["whoami"]["example"],
                  signature=command_data["whoami"]["signature"])
async def whoami(ctx):
    embed = discord.Embed(title="Information", color=0x00ff00)
    embed.description = "Hello, so you're curious who these bots are? Well, I'm glad you asked!\n\n" \
                        "**Who Is <@1116065332235358308>?**\nWell. This bot is our primary testing bot, a " \
                        "development " \
                        "one! " \
                        "This bot is used to test new features, commands, and more before they are pushed" \
                        " to the main " \
                        "bot.\n\n" \
                        "**Who Is <@741697357371932685>?**\nThis bot is our main bot, the one that is" \
                        " used in the " \
                        "server. " \
                        "This bot is the one that has all the commands, features, and more that you see in the " \
                        "server.\n\n" \
                        "**Who Is <@1114556584887078942>?**\nThis bot is our secondary testing bot, a development " \
                        "one! " \
                        "This bot is used to test new features, commands, and more before they are pushed to the " \
                        "primary testing bot.\n\n" \
                        "**Why Are There Three Bots?**\nWell, we have three bots for a few reasons. One, we want to " \
                        "test new features " \
                        "before they are pushed to the main bot. Two, we want to have a bot that is always online, " \
                        "even when we are " \
                        "working on the main bot. Three, we want to have a bot that is always online, even when we " \
                        "are working on the " \
                        "development bot.\n\n**What Is The Difference Between The Bots?**\nWell, the main bot is the " \
                        "one that is used " \
                        "in the server. The development bot is the one that is used to test new features, commands, " \
                        "and more before they " \
                        "are pushed to the main bot. The third bot is the one that is always online, even" \
                        " when we are " \
                        "working on the main " \
                        "bot or the development bot.\n\n**What Is The Third Bot?**\nThe third bot is the one that is " \
                        "always online, even " \
                        "when we are working on the main bot or the development bot. This bot is the one that" \
                        " is used " \
                        "to test new features, " \
                        "commands, and more before they are pushed to the main bot. This bot is the one that is used " \
                        "in the server. This bot " \
                        "is the one that has all the commands, features, and more that you see in the server."
    embed.add_field(name="What Can I Do?", value="I can do a lot of things, but here are some of my main features:\n"
                                                 "- Moderation\n"
                                                 "- Verification\n"
                                                 "- Auto-Role\n"
                                                 "- Auto-Mod\n"
                                                 "- Suggestions\n"
                                                 "- Reminders\n"
                                                 "- Logging\n"
                                                 "- Fun Commands\n"
                                                 "- And More!")
    embed.set_footer(text="If you have any questions, please contact @notk_ira or @robinthebank125 "
                          "or send 'I need help' to this bot.")
    embed.timestamp = ctx.message.created_at
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(whoami)
