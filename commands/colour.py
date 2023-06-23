import discord
from discord.ext import commands


@commands.command()
async def colour(ctx, colour: str):
    # Check if the input is in hexadecimal format
    if colour.startswith("#"):
        colour = colour[1:]  # Remove the "#" prefix

        # Convert the input color from hexadecimal to decimal RGB values
        r = int(colour[0:2], 16)
        g = int(colour[2:4], 16)
        b = int(colour[4:6], 16)
    else:
        # Parse the input color as comma-separated RGB values
        try:
            r, g, b = map(int, colour.split(","))
        except ValueError:
            await ctx.send(
                "Invalid input format. Please provide a valid hexadecimal color or comma-separated RGB values.")
            return

        # Convert RGB values to hexadecimal representation
        colour = f"{r:02x}{g:02x}{b:02x}"

    colour = colour.upper()  # Convert the hexadecimal color to uppercase
    # Create an embed with the specified color
    embed = discord.Embed(title="Colour", color=discord.Color.from_rgb(r, g, b))
    embed.add_field(name="Red", value=str(r))
    embed.add_field(name="Green", value=str(g))
    embed.add_field(name="Blue", value=str(b))
    embed.set_footer(text=f"Hex: #{colour}")
    embed.timestamp = ctx.message.created_at

    # Send the embed
    await ctx.send(embed=embed)


def setup(bot):
    bot.add_command(colour)
