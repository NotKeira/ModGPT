import discord
from discord.ext import commands

from database import Database

db = Database()

command_data = db.read_command_data()


def is_staff(ctx):
    user_id = str(ctx.author.id)
    user_data = Database().read_user_data()

    if user_id in user_data:
        user_info = user_data[user_id]
        iss = user_info.get("staff", False)
        return iss
    else:
        return False


@commands.command(help=command_data["staff"]["help"], example=command_data["staff"]["example"],
                  signature=command_data["staff"]["signature"])
async def staff(ctx, option=None):
    if is_staff(ctx):
        if option is None:
            embed = discord.Embed(title="Staff Commands", description="Here are the staff commands.",
                                  color=discord.Color.green())
            embed.add_field(name="server_list", value="Lists all servers the bot is in.")
            embed.add_field(name="server_info", value="Gives info about the server the command is ran in.")
            embed.add_field(name="user_list", value="Lists all users the bot has seen.")
            await ctx.send(embed=embed)
            return

        elif option.lower() == "server_list":
            embed = discord.Embed(title="Servers the bot is in",
                                  color=discord.Color.green())
            embed.description = ""
            for guild in ctx.bot.guilds:
                embed.description = embed.description + f"{guild.name} -> ({guild.id})\n"
            await ctx.send(embed=embed)
        elif option.lower() == "server_info":
            max_members = str(ctx.guild.max_members)
            if len(max_members) > 3:
                max_members = max_members[:len(max_members) - 3] + "," + max_members[len(max_members) - 3:]

            features = ctx.guild.features
            list_of_features = ""
            for i in features:
                i = i.replace("_", " ")
                i = i.title()
                list_of_features += f"- {i}\n"



            embed = discord.Embed(color=discord.Color.green())
            embed.description = "# Server Info \n"

            embed.description += f"**Name:** {ctx.guild.name}\n"
            embed.description += f"**ID:** {ctx.guild.id}\n"
            embed.description += f"**Owner:** {ctx.guild.owner}\n"
            embed.description += f"**Owner ID:** {ctx.guild.owner_id}\n"
            embed.description += f"**Member Count:** {ctx.guild.member_count}\n"
            embed.description += f"**Created At:** {ctx.guild.created_at}\n"

            embed.description += "## Security\n"

            embed.description += f"**Verification Level:** {ctx.guild.verification_level}\n"
            embed.description += f"**Explicit Content Filter:** {ctx.guild.explicit_content_filter}\n"
            embed.description += f"**2FA Level:** {ctx.guild.mfa_level}\n"

            embed.description += "## Limits\n"

            embed.description += f"**Max Members:** {max_members}\n"
            embed.description += f"**Max Presences:** {ctx.guild.max_presences}\n"
            embed.description += f"**Max Video Channel Users:**" \
                                 f" {ctx.guild.max_video_channel_users}\n"

            embed.description += "## Channels\n"

            embed.description += f"**Rules Channel:** " \
                                 f"{ctx.guild.rules_channel or 'No channel has been configured'}\n"
            embed.description += f"**System Channel:** " \
                                 f"{ctx.guild.system_channel or 'No channel has been configured'}\n"
            embed.description += f"**Public Updates Channel:** " \
                                 f"{ctx.guild.public_updates_channel or 'No channel has been configured'}\n"
            embed.description += f"**AFK Channel:** " \
                                 f"{ctx.guild.afk_channel or 'No channel has been configured'}\n"

            embed.description += "## Discovery\n"

            embed.description += f"**Description:** {ctx.guild.description or 'No Description set'}\n"
            embed.description += f"**Banner:** {ctx.guild.banner or 'No Banner set'}\n"
            embed.description += f"**Discovery Splash:** " \
                                 f"{ctx.guild.discovery_splash or'No Discovery Splash set'}" \
                                 f"\n"
            embed.description += f"**Splash:** {ctx.guild.splash}\n"

            embed.description += "## Miscellaneous\n"

            embed.description += f"**Is Large:** {ctx.guild.large}\n"
            embed.description += f"**AFK Timeout:** {ctx.guild.afk_timeout}\n"
            embed.description += f"**Default Notifications:** {ctx.guild.default_notifications}\n"
            embed.description += f"**Features:** \n{list_of_features}\n"
            embed.description += f"**Preferred Locale:**" \
                                 f" {ctx.guild.preferred_locale}\n"
            embed.description += f"**Premium Subscription Count:**" \
                                 f" {ctx.guild.premium_subscription_count}\n"
            embed.description += f"**Premium Tier:** {ctx.guild.premium_tier}\n"

            await ctx.send(embed=embed)
        elif option.lower() == "user_list":
            embed = discord.Embed(title="Users the bot has seen",
                                  color=discord.Color.green())
            embed.description = ""
            for user in ctx.bot.users:
                embed.description = embed.description + f"`{user.name}` -> ({user.id})\n"
            await ctx.send(embed=embed)

        else:
            await ctx.send("That is not a valid option.")
    else:
        await ctx.send("This command can only be used by staff members.")


@staff.error
async def staff_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to use this command.")


def setup(bot):
    bot.add_command(staff)
