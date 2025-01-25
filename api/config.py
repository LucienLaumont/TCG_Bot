import os
from dotenv import load_dotenv

load_dotenv()  # Charger les variables d'environnement depuis un fichier .env

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")