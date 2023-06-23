import asyncio
import math
import random
import time

import discord

from database import Database
from main import bot

db = Database()


async def blacklisted(raw):
    messageContent = []
    for i in raw.content.split(" "):
        messageContent.append(i)
    words = db.read_blacklisted_words()
    for i in words['words']:
        if i in messageContent:
            await raw.delete()
            await raw.channel.send('You cannot say that word here.')
            return
        else:
            continue


async def make_ticket_channel(message, identifier, guild, ticket_id):
    support_category = discord.utils.get(guild.categories, name="Support Tickets")
    if support_category is None:
        support_category = await guild.create_category("Support Tickets")
    channel = await guild.create_text_channel(f"ticket-{message.author.id}-{identifier}", category=support_category)
    data = {"user_id": message.author.id, "channel_id": channel.id, "staff": {}}
    db.add_ticket(data, ticket_id)
    print("Created ticket channel")
    embed = discord.Embed(title="New Ticket", description=message.content, color=discord.Color.blue())
    embed.set_footer(text=f"Ticket ID: {channel.name}")
    embed.timestamp = message.created_at
    await channel.send(embed=embed)
    return channel.name


def get_ticket_channel(message, guild):
    for channel in guild.channels:
        if not channel.name.startswith("ticket-"):
            continue
        name = channel.name.split("-")
        if name[1] == str(message.author.id):
            return channel.name


async def ticket_channel(message, guild, identifier, ticket_id):
    support_channel_name = get_ticket_channel(message, guild)
    if support_channel_name is None:
        ticket_name = await make_ticket_channel(message, identifier, guild, ticket_id)
        support_channel = discord.utils.get(guild.channels, name=ticket_name)
        await message.channel.send("Contacting the support team now!")
        embed = discord.Embed(title="New Ticket", description=message.content, color=discord.Color.blue())
        embed.set_footer(text=f"User: {message.author.id} - {message.author}")
        embed.timestamp = message.created_at
        await support_channel.send("@here", embed=embed)
    else:
        support_channel = discord.utils.get(guild.channels, name=support_channel_name)
        await message.channel.send("Sent your message to the support team!")
        embed = discord.Embed(title="New Reply", description=message.content, color=discord.Color.blue())
        embed.set_footer(text=f"User ID: {message.author.id} - {message.author}")
        embed.timestamp = message.created_at
        await support_channel.send(embed=embed)


async def handle_on_message(message):
    await blacklisted(message)
    if message.author == bot.user:
        return
    else:
        support_guild = bot.get_guild(715685846283452466)
        identifier = random.randint(1000, 9999)
        ticket_id = random.randint(1000000000000, 9999999999999)
        if isinstance(message.channel, discord.DMChannel) and message.author != bot.user:
            await ticket_channel(message, support_guild, identifier, ticket_id)
            for char in message.content:
                if len(message.content) > 2:
                    if char[0] == "t" and char[1] == "!" or char[0] == "r" and char[1] == "!":
                        await message.channel.send("You cannot use the ticket commands in a DM.")
                        return
        else:
            for ticket_id, ticket_data in db.get_ticket_data().items():
                if message.channel.id == int(ticket_data['channel_id']):
                    content = message.content
                    for c in content.split(" "):
                        if c == "t!staff":
                            staff = ""
                            for staff_id, staff_name in ticket_data['staff'].items():
                                staff += f"<@{staff_id}> \n"
                            if staff == "":
                                staff = "No staff."
                            embed = discord.Embed(
                                title="Staff",
                                description=staff,
                                color=discord.Color.blue()
                            )
                            await message.channel.send(embed=embed)
                            return
                        if c == "t!add":
                            identity = random.randint(0,9999999999)
                            user = ""
                            for char in content[8: len(content) - 1]:
                                user += char
                            user = await bot.fetch_user(int(user))
                            if user.id in ticket_data['staff']:
                                await message.channel.send(f"{user.name} is already in the ticket.")
                                return
                            ticket_data['staff'][str(user.id)] = user.name
                            db.edit_ticket(ticket_id, ticket_data)
                            await message.channel.send(f"Added {user.name} to the ticket.")
                            return
                        if c == "t!remove":
                            user = ""
                            for char in content[11: len(content) - 1]:
                                user += char
                            user = await bot.fetch_user(int(user))
                            if user.id not in ticket_data['staff']:
                                await message.channel.send(f"{user.name} is not in the ticket.")
                                return
                            ticket_data['staff'].pop(str(user.id))
                            db.edit_ticket(ticket_id, ticket_data)
                            await message.channel.send(f"Removed {user.name} from the ticket.")
                            return
                        if c == "t!close":
                            reason = ""
                            for char in content[8: len(content)]:
                                reason += char

                            embed = discord.Embed(
                                title="Ticket Closed",
                                color=discord.Color.blue()
                            )
                            embed.set_footer(text=f"Ticket ID: {message.channel.name}")
                            embed.timestamp = message.created_at
                            staff = ""
                            for staff_id, staff_name in ticket_data['staff'].items():
                                staff += f"<@{staff_id}> "
                            if staff == "":
                                staff = "No staff."
                            embed.description = f"**Ticket ID:** {message.channel.name}\n" \
                                                f"**Staff:** {staff}\n" \
                                                f"**Closed by:** {message.author.name}\n" \
                                                f"**Closed at:** <t:{math.floor(time.time())}:F>\n" \
                                                f"**Reason:** {reason}\n" \
                                                f"\n**Ticket closed by staff.**\n" \
                                                f"\n**If you have any questions, please contact the staff team.**"

                            await message.channel.send(embed=embed)
                            await bot.get_user(int(ticket_data['user_id'])).send(embed=embed)
                            # await bot.get_user(int(ticket_data['user_id'])).send(
                            #     f"Your ticket has been closed.\n"
                            #     f"Thank you for using the support system."
                            #     f"\n\n**Ticket ID:**"
                            #     f" {message.channel.name}"
                            #     f"\n**Staff:** {staff}"
                            #     f"\n**Closed by:** {message.author.name}"
                            #     f"\n**Closed at:** "
                            #     f"<t:{math.floor(time.time())}:F>"
                            #     f"\n\n**Ticket closed by staff.**"
                            #     f"\n\n**If you have any questions,"
                            #     f" please contact the staff team.**")

                            # Make a confirmation message to ask if they're sure they want to close the ticket.
                            # If they say yes, close the ticket.
                            # If they say no, delete the confirmation message and do nothing.
                            # If they don't respond, delete the confirmation message and do nothing.

                            await message.channel.send("Are you sure you want to close this ticket? (y/n)")

                            def check(m):
                                return m.author == message.author and m.channel == message.channel

                            try:
                                msg = await bot.wait_for('message', check=check, timeout=30)
                            except asyncio.TimeoutError:
                                await message.channel.send("You took too long to respond.")
                                await asyncio.sleep(5)
                                await message.channel.delete()
                                db.delete_ticket(ticket_id)
                                return
                            if msg.content.lower() == "y" or msg.content.lower() == "yes":
                                await message.channel.delete()
                                db.delete_ticket(ticket_id)
                                return
                            elif msg.content.lower() == "n" or msg.content.lower() == "no":
                                await message.channel.send("Ticket close cancelled.")
                                return
                            else:
                                await message.channel.send("Invalid response. Ticket close cancelled.")
                                return

                        if c == "t!r" or c == "t!reply":
                            # if message.author.id not in ticket_data['staff']:
                            #     await message.channel.send("You are not in this ticket.")
                            #     return
                            if c == "t!r":
                                content = content[4:]
                            else:
                                content = content[8:]

                            capitalized_content = content.capitalize()
                            embed = discord.Embed(
                                title="New Reply",
                                description=capitalized_content,
                                color=discord.Color.blue()
                            )
                            embed.set_footer(text=f"Staff: {message.author.top_role}")
                            embed.timestamp = message.created_at
                            await bot.get_user(int(ticket_data['user_id'])).send(embed=embed)
                            staff_embed = discord.Embed(
                                title="Reply Sent",
                                color=discord.Color.blue()
                            )
                            staff_embed.description = f"**Reply sent to:** " \
                                                      f"{bot.get_user(int(ticket_data['user_id'])).name}\n" \
                                                      f"**Reply sent at:** <t:{math.floor(time.time())}:F>\n" \
                                                      f"**Reply:** {capitalized_content}" \
                                                      f"\n\n**Staff:** {message.author.name} " \
                                                      f"- {message.author.top_role}"
                            staff_embed.set_footer(text=f"Ticket ID: {message.channel.name}")
                            await message.channel.send("Reply sent.", embed=staff_embed)
                            return
                        else:
                            return


def setup(bot):
    bot.add_listener(handle_on_message, 'on_message')
