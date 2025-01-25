import discord
from discord.ext import commands
from config import BOT_TOKEN
import os

# Initialisation du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Charger les commandes et événements automatiquement
for folder in ["commands", "events"]:
    for file in os.listdir(folder):
        if file.endswith(".py") and not file.startswith("__"):
            bot.load_extension(f"{folder}.{file[:-3]}")

# Lancer le bot
bot.run(BOT_TOKEN)