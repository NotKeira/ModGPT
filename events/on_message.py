import random

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


async def make_ticket_channel(message, identifier, guild):
    support_category = discord.utils.get(guild.categories, name="Support")
    if support_category is None:
        support_category = await guild.create_category("Support")
    channel = await guild.create_text_channel(f"ticket-{message.author.id}-{identifier}", category=support_category)
    data = {"user_id": message.author.id, "channel_id": channel.id, "staff": {}}
    db.add_ticket(data, identifier)
    return f"ticket-{message.author.id}-{identifier}"


def get_ticket_channel(message, support_server):
    for channel in support_server.channels:
        for i in channel.name.split("-"):
            if i == message.author.id:
                return channel.name


async def ticket_channel(message, guild, identifier):
    support_channel = discord.utils.get(guild.channels, name=get_ticket_channel(message, guild))
    if support_channel is None:
        ticket_name = await make_ticket_channel(message, identifier, guild)
        support_channel = discord.utils.get(guild.channels, name=ticket_name)
        return await message.channel.send("Contacting the support team now!")

    if support_channel is not None:
        await message.channel.send("Sent your message to the support team!")
        embed = discord.Embed(title="New Reply", description=message.content, color=discord.Color.blue())
        embed.set_footer(text=f"User ID: {message.author.id}")
        embed.timestamp = message.created_at
        await support_channel.send(embed=embed)
        return
    return await message.channel.send("Something went wrong, please try again later.")

async def applications(message, user):
    if message.content.lower() == "staff application":
        questions = {
            "age": "What is your age?",
            "timezone": "What is your timezone?",
            "experience": "What experience do you have?",
            "why": "Why do you want to be a  staff member?",
            "what": "What can you bring to the team?",
            "anything": "Anything else you would like to add?"
        }
        responses = {
            "age": "",
            "timezone": "",
            "experience": "",
            "why": "",
            "what": "",
            "anything": ""
        }
        embed = discord.Embed(
            title="Staff Application",
            description="Please answer the following questions to apply for the staff role.",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"User ID: {message.author.id}")
        embed.timestamp = message.created_at
        await user.send(embed=embed)
        for question, question_text in questions.items():
            await user.send(question_text)
            response = await bot.wait_for('message', check=lambda m: m.author == message.author)
            responses[question] = response.content
        embed = discord.Embed(
            title="Staff Application",
            description="Thank you for applying for the staff role. Your application has been "
                        "sent to the staff team.",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"User ID: {message.author.id}")
        embed.timestamp = message.created_at
        await user.send(embed=embed)
        embed = discord.Embed(
            title="New Staff Application",
            description="A new staff application has been submitted.",
            color=discord.Color.blue()
        )
        embed.add_field(name="Age", value=responses['age'])
        embed.add_field(name="Timezone", value=responses['timezone'])
        embed.add_field(name="Experience", value=responses['experience'])
        embed.add_field(name="Why", value=responses['why'])
        embed.add_field(name="What", value=responses['what'])
        embed.add_field(name="Anything", value=responses['anything'])
        embed.set_footer(text=f"User ID: {message.author.id}")
        embed.timestamp = message.created_at
        r = await message.channel.send(embed=embed)
        await r.add_reaction("✅")
        await r.add_reaction("❌")
        return


async def handle_on_message(message):
    await blacklisted(message)
    support_guild = bot.get_guild(997820212369948682)
    identifier = random.randint(1000, 9999)
    if message.channel.type == discord.ChannelType.private and message.author != bot.user:
        if message.content.startswith('r!'):
            return
        await ticket_channel(message, support_guild, identifier)
        if message.content.lower() == "i need help with the bot":
            await message.channel.send("Please wait while I contact the support team!")
        if message.content.lower() == "staff application":
            user = bot.get_user(int(message.author.id))
            return await applications(message, user)
    else:
        if message.author == bot.user:
            return
        for ticket_id, ticket_data in db.get_ticket_data().items():
            if message.channel.id == int(ticket_data['channel_id']):
                content = message.content

                if content == "t!add":
                    pass
                if content == "t!remove":
                    pass
                if content == "t!rename":
                    pass
                if content == "t!close":
                    await message.channel.send("Closing the ticket in 5 seconds...") and await bot.get_user(
                        int(ticket_data['user_id'])).send("Closing the ticket in 5 seconds...")
                    await message.channel.send("4...")
                    await message.channel.send("3...")
                    await message.channel.send("2...")
                    await message.channel.send("1...")
                    await message.channel.send("Ticket closed!") and await bot.get_user(
                        int(ticket_data['user_id'])).send("Ticket closed!")
                    await message.channel.delete()
                    db.delete_ticket(ticket_id)
                    return
                capitalized_content = content[0].capitalize() + content[1:]
                embed = discord.Embed(
                    title="New Reply",
                    description=capitalized_content,
                    color=discord.Color.blue()
                )
                embed.set_footer(text=f"Staff ID: {message.author.id}")
                embed.timestamp = message.created_at
                await bot.get_user(int(ticket_data['user_id'])).send(embed=embed)
                return


def setup(bot):
    bot.add_listener(handle_on_message, 'on_message')
