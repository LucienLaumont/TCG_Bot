import discord
import httpx
from discord.ext import commands
from sqlalchemy.orm import Session
from random import randint
from .utils import compare_numeric_values
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
        response = await client.get(f"{NGROK_URL}/api/player/{discord_id}")
        print(f"{NGROK_URL}/api/player/{discord_id}")        
        if response.status_code == 200:
            await ctx.send(f"{ctx.author.mention}, vous êtes déjà enregistré dans la base de données.")
        elif response.status_code == 404:
            # Créer un nouveau joueur via l'API
            data = {"discord_id": discord_id, "player_name": player_name}
            print(data)    
            create_response = await client.post(f"{NGROK_URL}/api/player/", json=data)
            print(create_response)
            if create_response.status_code == 200:
                await ctx.send(f"{ctx.author.mention}, vous avez été enregistré avec succès dans la base de données !")
            else:
                await ctx.send(f"{ctx.author.mention}, une erreur s'est produite lors de votre enregistrement.")
        else:
            await ctx.send(f"{ctx.author.mention}, une erreur inattendue s'est produite. Veuillez réessayer plus tard.")

@bot.command(name="pokedl")
async def pokedl(ctx):
    discord_id = str(ctx.author.id)

    async with httpx.AsyncClient() as client:
        # Vérifie si le joueur est déjà enregistré
        response = await client.get(f"{NGROK_URL}/api/player/{discord_id}")
        
        if response.status_code == 404:
            await ctx.send(f"{ctx.author.mention}, vous n'êtes pas encore enregistré dans la base de données.\nLancez la commande **!register**.")
        elif response.status_code == 200:
            # Récupérer un Pokémon aléatoire
            pokedex_number = randint(1, 801)
            pokemon_response = await client.get(f"{NGROK_URL}/api/pokemon/{pokedex_number}")
            
            if pokemon_response.status_code != 200:
                await ctx.send(f"{ctx.author.mention}, impossible de récupérer les informations du Pokémon.")
                return

            # Initialiser uniquement avec discord_id et pokedex_number
            session_data = {
                "discord_id": discord_id,
                "pokedex_number": pokedex_number
            }

            # Créer une nouvelle session via l'API
            session_response = await client.post(f"{NGROK_URL}/api/pokemonsession/", json=session_data)
            
            if session_response.status_code == 200:
                # Afficher un embed avec les champs vides (ou ? si manquant)
                embed = discord.Embed(
                    title="Session Pokémon : Trouvez les bonnes réponses !",
                    description="La session a commencé ! Essayez de deviner les informations du Pokémon.",
                    color=discord.Color.red()
                )

                # Définir les catégories avec un ? car elles sont initialisées à Null
                categories = {
                    "Nom (FR)": " ",
                    "Type 1": " ",
                    "Type 2": " ",
                    "Évolution": " ",
                    "Poids (kg)": " ",
                    "Taille (m)": " ",
                    "Génération": " ",
                    "Classification": " ",
                }

                # Ajouter chaque champ à l'embed avec le carré rouge
                for category, answer in categories.items():
                    embed.add_field(
                        name=f"**{category} : {answer}**",
                        value="🟥",
                        inline=True
                    )

                # Envoyer l'embed au joueur
                await ctx.send(embed=embed)
            else:
                # En cas d'erreur lors de la création de la session
                error_message = session_response.json().get("detail", "Erreur inconnue")
                await ctx.send(f"{ctx.author.mention}, une erreur s'est produite lors de la création de la session : {error_message}")
        else:
            await ctx.send(f"{ctx.author.mention}, une erreur inattendue s'est produite. Veuillez réessayer plus tard.")

@bot.command(name="guess")
async def guess(ctx, *, pokemon_guess: str):
    discord_id = str(ctx.author.id)

    async with httpx.AsyncClient() as client:
        # Vérifier si le joueur a une session active
        session_response = await client.get(f"{NGROK_URL}/api/pokemonsession/active/{discord_id}")

        if session_response.status_code == 404:
            await ctx.send(f"{ctx.author.mention}, vous n'avez pas de session en cours.\nLancez la commande **!pokedl** pour commencer une session.")
            return

        # Récupérer les données de la session actuelle
        session_data = session_response.json()
        pokedex_number_target = session_data['pokedex_number']

        # Récupérer les informations du Pokémon cible (à deviner)
        target_pokemon_response = await client.get(f"{NGROK_URL}/api/pokemon/{pokedex_number_target}")
        if target_pokemon_response.status_code == 404:
            await ctx.send(f"{ctx.author.mention}, une erreur est survenue. Le Pokémon cible est introuvable.")
            return
        target_pokemon = target_pokemon_response.json()

        # Rechercher le Pokémon deviné
        search_response = await client.get(f"{NGROK_URL}/api/pokemon/search/?name={pokemon_guess}")
        if search_response.status_code == 404:
            await ctx.send(f"{ctx.author.mention}, aucun Pokémon trouvé avec ce nom. Essayez encore.")
            return

        guessed_pokemon = search_response.json()

        # Appeler l’API pour comparer les réponses et mettre à jour la session
        update_response = await client.put(f"{NGROK_URL}/api/pokemonsession/update/{discord_id}", json={"guessed_pokemon": guessed_pokemon})

        if update_response.status_code == 200:
            updated_session = update_response.json()

            # Créer l'embed avec les catégories mises à jour
            # Créer l'embed avec les catégories mises à jour
            embed = discord.Embed(
                title=f"Session Pokémon : {ctx.author.name}",
                description="Voici votre progression dans la session actuelle.",
                color=discord.Color.green()
            )

            # Comparer les champs entre le Pokémon cible et le Pokémon soumis
            categories = {
                "name_fr": {"label": "Nom (FR)", "target_value": target_pokemon.get("name_fr"), "guessed_value": guessed_pokemon.get("name_fr")},
                "type1": {"label": "Type 1", "target_value": target_pokemon.get("type1"), "guessed_value": guessed_pokemon.get("type1")},
                "type2": {"label": "Type 2", "target_value": target_pokemon.get("type2"), "guessed_value": guessed_pokemon.get("type2")},
                "evolution": {"label": "Évolution", "target_value": target_pokemon.get("evolution"), "guessed_value": guessed_pokemon.get("evolution")},
                "weight_kg": {"label": "Poids (kg)", "target_value": target_pokemon.get("weight_kg"), "guessed_value": guessed_pokemon.get("weight_kg")},
                "height_m": {"label": "Taille (m)", "target_value": target_pokemon.get("height_m"), "guessed_value": guessed_pokemon.get("height_m")},
                "generation": {"label": "Génération", "target_value": target_pokemon.get("generation"), "guessed_value": guessed_pokemon.get("generation")},
                "classfication": {"label": "Classification", "target_value": target_pokemon.get("classfication"), "guessed_value": guessed_pokemon.get("classfication")},
            }

            for key, info in categories.items():
                if key in ["weight_kg", "height_m"]:
                    # Comparer les valeurs numériques si elles sont présentes
                    if info["target_value"] and info["guessed_value"]:
                        emoji = compare_numeric_values(info["target_value"], info["guessed_value"])
                    else:
                        emoji = "❓"  # Si les valeurs sont manquantes ou incorrectes
                else:
                    # Comparaison normale pour les autres champs
                    emoji = "🟩" if info["guessed_value"] == info["target_value"] else "🟥"

                # Déterminer la valeur à afficher
                value_display = info["guessed_value"] if info["guessed_value"] is not None else "?"

                # Ajouter le champ à l'embed
                embed.add_field(name=f"**{info['label']} : {value_display}**", value=f"{emoji} ", inline=True)

            # Envoyer l'embed au joueur
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}, une erreur s'est produite lors de la mise à jour de la session.")