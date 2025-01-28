import discord
from discord.ext import commands
from sqlalchemy.orm import Session
from api.database.database import get_db
from api.models.player import PlayerCreate
from api.services.player_service import get_player_by_discord_id, create_player

intents = discord.Intents.default()
intents.message_content = True  # Assurez-vous d'activer ceci dans le portail des développeurs Discord

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="register")
async def register(ctx):
    discord_id = ctx.author.id
    player_name = ctx.author.name

    # Connexion à la base de données
    db: Session = next(get_db())

    # Vérifie si le joueur est déjà enregistré
    player = get_player_by_discord_id(db, discord_id)
    if player:
        await ctx.send(f"{ctx.author.mention}, vous êtes déjà enregistré dans la base de données.")
    else:
        # Ajoute le joueur
        new_player = PlayerCreate(discord_id=discord_id, player_name=player_name)
        create_player(db, new_player)
        await ctx.send(f"{ctx.author.mention}, vous avez été enregistré avec succès dans la base de données !")
