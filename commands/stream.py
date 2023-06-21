from discord.ext import commands
import discord
@commands.command()
async def stream(ctx, opt):
    embed = discord.Embed(title="I'm Streaming", color=0x00ff00)
    if opt.lower() == "twitch":
        embed.description = "https://www.twitch.tv/notk_ira"
        embed.url = "https://www.twitch.tv/notk_ira"
    elif opt.lower() == "youtube":
        embed.description = "https://youtube.com/@notk_ira"
        embed.url = "https://youtube.com/@notk_ira"
    else:
        return ctx.send("Invalid option. Valid options are `twitch` and `youtube`.")
    await ctx.send("@everyone", embed=embed)

def setup(bot):
    bot.add_command(stream)