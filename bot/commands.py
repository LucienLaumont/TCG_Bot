import discord
import httpx
from discord.ext import commands
from sqlalchemy.orm import Session
from random import randint
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Récupérer l'URL Ngrok depuis le fichier .env
NGROK_URL = os.getenv("NGROK_URL")

# Vérifier si NGROK_URL est défini
if not NGROK_URL:
    raise ValueError("NGROK_URL is not defined in the .env file!")

@bot.command(name="register")
async def register(ctx):
    discord_id = str(ctx.author.id)
    player_name = ctx.author.name

    async with httpx.AsyncClient() as client:
        # Appel à l'API via l'URL Ngrok
        response = await client.get(f"{NGROK_URL}/player/{discord_id}")
        
        if response.status_code == 200:
            await ctx.send(f"{ctx.author.mention}, vous êtes déjà enregistré dans la base de données.")
        elif response.status_code == 404:
            # Créer un nouveau joueur via l'API
            data = {"discord_id": discord_id, "player_name": player_name}
            create_response = await client.post(f"{NGROK_URL}/player", json=data)
            
            if create_response.status_code == 201:
                await ctx.send(f"{ctx.author.mention}, vous avez été enregistré avec succès dans la base de données !")
            else:
                await ctx.send(f"{ctx.author.mention}, une erreur s'est produite lors de votre enregistrement.")
        else:
            await ctx.send(f"{ctx.author.mention}, une erreur inattendue s'est produite. Veuillez réessayer plus tard.")


@bot.command(name="pokedl")
async def pokedl(ctx):
    discord_id = str(ctx.author.id)

    async with httpx.AsyncClient() as client:
        # Vérifie si le joueur est déjà enregistré via l'API
        response = await client.get(f"{NGROK_URL}/player/{discord_id}")
        
        if response.status_code == 404:
            await ctx.send(f"{ctx.author.mention}, vous n'êtes pas encore enregistré dans la base de données. \nLancez la commande !register")
        elif response.status_code == 200:
            # Créer une nouvelle session via l'API
            data = {"discord_id": discord_id, "pokedex_number": randint(1, 801)}
            session_response = await client.post(f"{NGROK_URL}/pokemonsession", json=data)
            
            if session_response.status_code == 200:
                await ctx.send(f"{ctx.author.mention}, une nouvelle session a été créée avec succès !")
            else:
                # Récupère le message d'erreur renvoyé par l'API
                error_message = session_response.json().get("detail", "Erreur inconnue")
                await ctx.send(f"{ctx.author.mention}, une erreur s'est produite : {error_message}")
        else:
            await ctx.send(f"{ctx.author.mention}, une erreur inattendue s'est produite. Veuillez réessayer plus tard.")
        
