import psycopg2
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
dbname = os.getenv("DATABASE_NAME")

CSV_FILE = "pokemon.csv"
JSON_FILE = "pokemon.json"

def create_tables():

    # Connexion à la base PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Création de la table pokemon
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon (
                pokedex_number INTEGER PRIMARY KEY,
                name TEXT,
                name_fr TEXT,
                evolution INTEGER,
                type1 TEXT,
                type2 TEXT,
                weight_kg REAL,
                height_m REAL,
                generation INTEGER,
                is_legendary INTEGER,
                classfication TEXT
            )
        ''')

        # Création de la table player
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player (
                discord_id TEXT PRIMARY KEY,
                player_name TEXT NOT NULL UNIQUE,
                win_count INTEGER DEFAULT NULL,
                win_streak INTEGER DEFAULT NULL
            )
        ''')

        # Création de la table session avec les clés étrangères
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS session (
                id SERIAL PRIMARY KEY,
                discord_id TEXT NOT NULL,
                pokedex_number INTEGER NOT NULL,
                found INTEGER DEFAULT NULL,
                name TEXT,
                name_fr TEXT,
                evolution INTEGER DEFAULT NULL,
                type1 TEXT,
                type2 TEXT DEFAULT NULL,
                weight_kg REAL,
                height_m REAL,
                generation INTEGER,
                is_legendary INTEGER,
                classfication TEXT,
                FOREIGN KEY (discord_id) REFERENCES player(discord_id) ON DELETE CASCADE,
                FOREIGN KEY (pokedex_number) REFERENCES pokemon(pokedex_number) ON DELETE CASCADE
            )
        ''')

        # Validation des changements
        conn.commit()
        print("Les tables ont été créées avec succès.")

    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()

def preprocess_pokemon_data(csv_file, json_file):

    # Charger les données depuis le fichier CSV
    pokemon_data = pd.read_csv(csv_file, delimiter=',')

    # Charger les données JSON contenant les noms et niveaux d'évolution
    with open(json_file, 'r', encoding='utf-8') as file:
        pokemon_json_data = json.load(file)

    # Création d'un dictionnaire de traduction des noms anglais vers les noms français
    name_translation = {
        entry['name']['en']: entry['name']['fr']
        for entry in pokemon_json_data if 'name' in entry
    }

    # Ajouter la colonne `name_fr` au DataFrame
    pokemon_data['name_fr'] = pokemon_data['name'].map(name_translation)

    # Création d'un dictionnaire associant les noms anglais des Pokémon à leur niveau d'évolution
    evolution_levels = {}

    for entry in pokemon_json_data:
        if 'name' in entry and isinstance(entry.get('evolution'), dict):
            name_en = entry['name']['en']
            evolution_data = entry['evolution']

            # Déterminer le niveau d'évolution
            if evolution_data.get('pre') is None and evolution_data.get('next') is not None:
                evolution_levels[name_en] = 1  # Pokémon de base
            elif evolution_data.get('pre') is not None and evolution_data.get('next') is not None:
                evolution_levels[name_en] = 2  # Pokémon intermédiaire
            elif evolution_data.get('next') is None:
                evolution_levels[name_en] = 3  # Pokémon final
        else:
            # Si le champ 'evolution' est manquant ou n'est pas un dictionnaire
            name_en = entry['name']['en']
            evolution_levels[name_en] = 1  # Niveau inconnu ou non applicable

    # Ajouter la colonne `evolution` au DataFrame
    pokemon_data['evolution'] = pokemon_data['name'].map(evolution_levels)

    # Liste des colonnes à conserver
    colonnes_a_conserver = [
        'pokedex_number', 'name', 'name_fr', 'evolution', 'type1', 'type2',
        'weight_kg', 'height_m', 'generation', 'is_legendary', 'classfication'
    ]

    # Création d'un nouveau DataFrame avec les colonnes sélectionnées
    pokemon_selection = pokemon_data[colonnes_a_conserver]

    # Nettoyage des données manquantes (optionnel, si nécessaire)
    pokemon_selection.fillna({'type2': 'None', 'classfication': 'Unknown'}, inplace=True)

    return pokemon_selection

def insert_pokemon_data_to_db(dataframe):

    load_dotenv()

    try:
        # Connexion à la base de données
        conn = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        # Préparation de la requête d'insertion
        insert_query = """
        INSERT INTO pokemon (
            pokedex_number, name, name_fr, evolution, type1, type2,
            weight_kg, height_m, generation, is_legendary, classfication
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (pokedex_number) DO NOTHING;
        """

        # Insertion des données
        for _, row in dataframe.iterrows():
            cursor.execute(insert_query, (
                row['pokedex_number'], row['name'], row['name_fr'], row['evolution'],
                row['type1'], row['type2'], row['weight_kg'], row['height_m'],
                row['generation'], row['is_legendary'], row['classfication']
            ))

        # Validation des changements
        conn.commit()
        print("Insertion des données terminée avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()


def main():

    # Prétraitement des données
    preprocessed_data = preprocess_pokemon_data(CSV_FILE, JSON_FILE)

    # Insertion des données dans la base de données
    insert_pokemon_data_to_db(preprocessed_data)

if __name__ == "__main__":
    main()
