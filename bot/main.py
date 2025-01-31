import os
from discord.ext import commands
from bot.commands import bot

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)
