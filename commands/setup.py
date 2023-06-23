import asyncio
import time

import discord
from discord.ext import commands

from database import Database
from main import bot

db = Database()


async def push_data(guild, data):
    print(data)
    try:
        guild = bot.get_guild(guild)

        guild_data = db.read_guild_data()
        db.set_value(guild_data, str(guild.id), data)
        db.write_guild_data(guild_data)
        return True
    except ValueError:
        print("Invalid guild ID. The bot does not have access to the specified guild.")


async def create_required(guild, options):
    data = {
        'prefix': 'r!',
        'welcome_message': 'Welcome to the server!',
        'admin_roles': {},
        'member_role': '',
        'muted_role': '',
        'audit_logs': '',
        'welcome-channel': '',
    }
    print(data)

    def check_if_exists(opt, name):
        if opt == "channel":
            for i in guild.channels:
                if i.name == name:
                    return True
            return False
        elif opt == "category":
            for i in guild.categories:
                if i.name == name:
                    return True
            return False
        elif opt == "role":
            for i in guild.roles:
                if i.name == name:
                    return True
            return False

    # Categories
    if not check_if_exists("category", "Audit Logs") and options["audit-logs"]:
        audit_logs_category = await guild.create_category("Audit Logs", reason="Setting up the server")
    # Channels
    if not check_if_exists("channel", "welcome") and options["welcome"]:
        welcome = await guild.create_text_channel("welcome", reason="Setting up the server")
        data["welcome"] = welcome.id

    if not check_if_exists("channel", "audit-logs") and options["audit-logs"]:
        audit_logs_category = discord.utils.get(guild.categories, name="Audit Logs")
        audit = await guild.create_text_channel("audit-logs", category=audit_logs_category,
                                                reason="Setting up the server")
        data["audit-logs"] = audit.id
        # Roles
    if not check_if_exists("role", "Muted"):
        muted = await guild.create_role(name="Muted", mentionable=False, hoist=True,
                                        permissions=discord.Permissions.none(),
                                        reason="Setting up the server")
        data["muted"] = muted.id
    if not check_if_exists("role", "Member"):
        member = await guild.create_role(name="Member", mentionable=False, hoist=True, reason="Setting up the server")
        data["member"] = member.id

    print(data)


class Setup(commands.Cog):
    def __init__(self, bo):
        self.bot = bo

    @commands.command()
    async def setup(self, ctx):
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == 801384603704623115:
            options = {
                "welcome": False,
                "audit-logs": False,

            }
            embed = discord.Embed(title="Setup",
                                  description="Welcome to the setup! Please select the options you want to enable.",
                                  color=0x00ff00)
            embed.add_field(name="Welcome", value="This includes the following: `Welcome Channel`, `Welcome Message`",
                            inline=False)
            embed.add_field(name="Audit Logs", value="This includes the following: `Audit Logs Category`, "
                                                     "`Audit Logs Channel`",
                            inline=False)
            embed.set_footer(
                text="You have 30 seconds to answer "
                     "each question. If you don't answer in time, the setup"
                     " will be cancelled. If you want to cancel the setup, type 'cancel'.")
            enabled = discord.Embed(title="Setup",
                                    description="**Options:**"
                                                "\n- Welcome: ❌"
                                                "\n- Audit Logs: ❌"
                                                # "\n- Support Tickets: ❌"
                                                "\n\nPlease select the options you want to enable.",
                                    color=0x00ff00)
            first_embed = await ctx.send(embed=embed)
            enabled_embed = await ctx.send(embed=enabled)
            reactions = ['✅', '❌']

            for option in options:
                opt = await ctx.send(f"Would you like to enable {option}?")

                for reaction in reactions:
                    await opt.add_reaction(reaction)

                def check(reac, user):
                    return (
                            user == ctx.author
                            and str(reac.emoji) in reactions
                            and reac.message.id == opt.id
                    )

                try:
                    reaction, _ = await bot.wait_for('reaction_add', timeout=30.0, check=check)
                    if str(reaction.emoji) == '✅':
                        options[option] = True
                        enabled.description = enabled.description.replace(f"- {option}: ❌", f"- {option}: ✅")
                        await enabled_embed.edit(embed=enabled)
                    elif str(reaction.emoji) == '❌':
                        options[option] = False
                        enabled.description = enabled.description.replace(f"- {option}: ❌", f"- {option}: ❌")
                    else:
                        await ctx.send("That's not a valid option, please rerun the command!")
                        return
                    await enabled_embed.edit(embed=enabled)
                    await opt.delete()
                except asyncio.TimeoutError:
                    await ctx.send("You didn't answer in time!")
                    return

            await first_embed.delete()
            em = discord.Embed(title="Setup",
                               description="Your setup is now complete! Please wait while I set everything up.",
                               color=0x00ff00)
            em.set_footer(text="This may take a minute so grab some popcorn and a chair!.")
            second_embed = await ctx.send(embed=em)
            current_time = time.time()
            setting_msg = await ctx.send("Setting up...")

            msg_categories = await ctx.send(content="Creating categories...")

            msg_channels = await ctx.send(content="Creating channels...")

            msg_roles = await ctx.send(content="Creating roles...")
            await create_required(bot.get_guild(ctx.guild.id), options)
            await asyncio.sleep(1)

            await msg_categories.edit(content="Categories created!")
            await msg_channels.edit(content="Channels created!")
            await msg_roles.edit(content="Roles created!")

            completed_message = await ctx.send(
                f"Setup complete! It took {round(time.time() - current_time, 2)} seconds.")

            await msg_roles.delete()
            await msg_channels.delete()
            await msg_categories.delete()
            await setting_msg.delete()
            await second_embed.delete()
            await completed_message.delete()
            await ctx.message.delete()

        else:
            await ctx.send("You don't have permission to do that!")


def setup(b):
    b.add_cog(Setup(b))
