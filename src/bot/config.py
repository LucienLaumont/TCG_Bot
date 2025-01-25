import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Variables globales
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")