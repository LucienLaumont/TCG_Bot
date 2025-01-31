import discord
import httpx
from discord.ext import commands
from discord import app_commands
from random import randint
from .utils import compare_numeric_values
import os

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix="!", intents=intents)

NGROK_URL = os.getenv("NGROK_URL")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not NGROK_URL:
    raise ValueError("NGROK_URL is not defined in the .env file!")

# Définir la fonction d’autocomplete
async def pokemon_autocomplete(interaction: discord.Interaction, current: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NGROK_URL}/api/pokemon/suggestions/?query={current}")

        if response.status_code == 200:
            suggestions = response.json()
            return [app_commands.Choice(name=s, value=s) for s in suggestions[:5]]
        return [app_commands.Choice(name="Aucun résultat", value="")]

class PokemonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pokeregister", description="Enregistrer un joueur dans la base de données.")
    async def pokeregister(self, interaction: discord.Interaction):
        discord_id = str(interaction.user.id)
        player_name = interaction.user.name

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NGROK_URL}/api/player/{discord_id}")
            if response.status_code == 200:
                await interaction.response.send_message(f"{interaction.user.mention}, vous êtes déjà enregistré.", ephemeral=True)
            elif response.status_code == 404:
                data = {"discord_id": discord_id, "player_name": player_name}
                create_response = await client.post(f"{NGROK_URL}/api/player/", json=data)
                if create_response.status_code == 200:
                    await interaction.response.send_message(f"{interaction.user.mention}, vous avez été enregistré avec succès !", ephemeral=True)
                else:
                    await interaction.response.send_message(f"{interaction.user.mention}, une erreur s'est produite lors de l'enregistrement.", ephemeral=True)
            else:
                await interaction.response.send_message(f"{interaction.user.mention}, une erreur inattendue s'est produite.", ephemeral=True)

    @app_commands.command(name="pokedl", description="Commencez une session de devinettes Pokémon.")
    async def pokedl(self, interaction: discord.Interaction):
        discord_id = str(interaction.user.id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NGROK_URL}/api/player/{discord_id}")
            if response.status_code == 404:
                await interaction.response.send_message(f"{interaction.user.mention}, vous n'êtes pas encore enregistré. Lancez **/pokeregister**.", ephemeral=True)
                return

            pokedex_number = randint(1, 801)
            pokemon_response = await client.get(f"{NGROK_URL}/api/pokemon/{pokedex_number}")
            if pokemon_response.status_code != 200:
                await interaction.response.send_message(f"{interaction.user.mention}, impossible de récupérer les informations du Pokémon.", ephemeral=True)
                return

            session_data = {"discord_id": discord_id, "pokedex_number": pokedex_number}
            session_response = await client.post(f"{NGROK_URL}/api/pokemonsession/", json=session_data)

            if session_response.status_code == 200:
                embed = discord.Embed(
                    title="Session Pokémon",
                    description="La session a commencé, devinez le Pokémon !",
                    color=discord.Color.red()
                )
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

                for category, answer in categories.items():
                    embed.add_field(name=f"**{category}**", value=f"🟥 {answer}", inline=True)

                await interaction.response.send_message(embed=embed)
            else:
                error_message = session_response.json().get("detail", "Erreur inconnue")
                await interaction.response.send_message(f"{interaction.user.mention}, erreur : {error_message}", ephemeral=True)

    @app_commands.command(name="pokeguess", description="Devinez le Pokémon de la session en cours.")
    @app_commands.autocomplete(pokemon=pokemon_autocomplete)
    async def pokeguess(self, interaction: discord.Interaction, pokemon: str):
        discord_id = str(interaction.user.id)

        async with httpx.AsyncClient() as client:
            session_response = await client.get(f"{NGROK_URL}/api/pokemonsession/active/{discord_id}")
            if session_response.status_code == 404:
                await interaction.response.send_message(
                    f"{interaction.user.mention}, lancez **/pokedl** pour commencer une session.", ephemeral=True
                )
                return

            session_data = session_response.json()
            pokedex_number_target = session_data['pokedex_number']
            target_pokemon_response = await client.get(f"{NGROK_URL}/api/pokemon/{pokedex_number_target}")
            target_pokemon = target_pokemon_response.json()

            search_response = await client.get(f"{NGROK_URL}/api/pokemon/search/?name={pokemon}")
            guessed_pokemon = search_response.json()

            embed = discord.Embed(
                title=f"Session Pokémon : {interaction.user.name}",
                description="Votre progression actuelle.",
                color=discord.Color.green()
            )

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
                emoji = "🟩" if info["guessed_value"] == info["target_value"] else "🟥"
                value_display = info["guessed_value"] if info["guessed_value"] else "?"
                embed.add_field(name=f"**{info['label']}**", value=f"{emoji} {value_display}", inline=True)

            await interaction.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

    # Ajouter les commandes slash
    await bot.add_cog(PokemonCommands(bot))
    await bot.tree.sync()

bot.run(DISCORD_BOT_TOKEN)
