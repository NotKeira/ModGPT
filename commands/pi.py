import asyncio

import discord
from discord.ext import commands

lyrics = [
    "Three point one four one five nine, this is Pi",
    "Followed by two-six-five-three-five-eight-nine",
    "Circumference over diameter",
    "Seven-nine, then three-two-three",
    "O-M-G, can't you see?",
    "Eight-four-six-two-six-four-three",
    "And now we're on a spree",
    "Thirty-eight and thirty-two, now we're blue",
    "Oh, who knew?",
    "Seven thousand nine hundred, fifty and then a two",
    "Eighty-eight and forty-one, so much fun",
    "Now a run",
    "Nine-seven-one-six-nine-three-nine-nine",
    "Three-seven-fifty-one",
    "Halfway done",
    "Zero-five-eight, now don't be late",
    "Two-zero-nine, where's the wine?",
    "Seven-four, it's on the floor",
    "Then nine-four-four-five-nine",
    "Two-three-zero, we gotta go",
    "Seven-eight, we can't wait",
    "One-six-four-zero-six-two-eight",
    "We're almost near the end, keep going",
    "Sixty-two, we're getting through",
    "Zero-eight-nine-nine, on time",
    "Eight-six-two-eight-zero-three-four",
    "There's only a few more",
    "Eight-two, then five-three",
    "Forty-two, eleven, seventy, and sixty-seven",
    "We're done, was that fun?",
    "Learning random digits",
    "So that you can brag to your friends"
]

from database import Database

db = Database()

command_data = db.read_command_data()


@commands.command(help=command_data["pi"]["help"], example=command_data["pi"]["example"],
                  signature=command_data["pi"]["signature"])
async def pi(ctx):
    for line in lyrics:
        await ctx.send(line)
        await asyncio.sleep(1)

def setup(bot):
    bot.add_command(pi)
