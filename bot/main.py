import os
from discord.ext import commands
from bot.commands.register import bot

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Ajoutez votre token ici ou dans un fichier .env

if __name__ == "__main__":
    bot.run(TOKEN)
