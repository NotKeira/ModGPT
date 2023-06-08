import discord

from database import CustomDatabase

db = CustomDatabase(guilds_file='guilds.json', users_file='users.json')


def setup(bot):
    command_data = db.read_command_data()

    @bot.command(help=command_data["admins"]["help"], example=command_data["admins"]["example"],
                 signature=command_data["admins"]["signature"])
    async def admins(ctx):
        guild_id = str(ctx.guild.id)
        guild_data = db.read_guild_data()

        if guild_id not in guild_data:
            await ctx.send("Guild data not found.")
            return

        data = guild_data[guild_id]
        roles = data.get("admin_roles", {})

        if not roles:
            await ctx.send("No roles found in the guild data.")
            return

        admin = [role_id for role_id, role_info in roles.items() if role_info.get("admin", False)]

        if not admin:
            await ctx.send("No admins found in the guild data.")
            return

        embed = discord.Embed(title="Admins in Guild Data", color=discord.Color.blue())
        for idx, admin_role_id in enumerate(admin, 1):
            role = ctx.guild.get_role(int(admin_role_id))
            if role:
                embed.add_field(name=f"Admin #{idx}", value=f"{role.name} - {role.id}", inline=False)

        await ctx.send(embed=embed)

    bot.add_command(admins)
