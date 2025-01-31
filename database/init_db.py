import json
import psycopg2
import os

user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
dbname = os.getenv("DATABASE_NAME")

JSON_FILE = "pokemon.json"

def create_tables(cursor):
    try:
        # Création de la table pokemon
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pokemon (
                pokedex_number INTEGER PRIMARY KEY,
                name TEXT,
                name_fr TEXT,
                evolution INTEGER,
                type1 TEXT,
                type2 TEXT,
                weight_kg TEXT,
                height_m TEXT,
                generation INTEGER,
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
            CREATE TABLE IF NOT EXISTS pokemonsession (
                id SERIAL PRIMARY KEY,
                discord_id TEXT NOT NULL,
                pokedex_number INTEGER NOT NULL,
                found INTEGER DEFAULT NULL,
                name TEXT,
                name_fr TEXT,
                evolution INTEGER DEFAULT NULL,
                type1 TEXT,
                type2 TEXT DEFAULT NULL,
                weight_kg TEXT,
                height_m TEXT,
                generation INTEGER,
                classfication TEXT,
                FOREIGN KEY (discord_id) REFERENCES player(discord_id) ON DELETE CASCADE,
                FOREIGN KEY (pokedex_number) REFERENCES pokemon(pokedex_number) ON DELETE CASCADE
            )
        ''')

        print("Les tables ont été créées avec succès.")

    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")

def parse_float(value):
    if value:
        # Supprimer les espaces, les unités et remplacer la virgule par un point
        return float(value.replace(" m", "").replace(" kg", "").replace(",", ".").strip())
    return None

def insert_pokemon_data(cursor):
    # Charger les données JSON
    with open(JSON_FILE, 'r', encoding='utf-8') as file:
        pokemon_data = json.load(file)

    # Préparer l'instruction SQL
    insert_query = """
    INSERT INTO pokemon (
        pokedex_number, name, name_fr, evolution, type1, type2,
        weight_kg, height_m, generation, classfication
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (pokedex_number) DO NOTHING;
    """

    # Traitement et insertion des données
    for pokemon in pokemon_data:
        pokedex_number = pokemon["pokedex_id"]
        name = pokemon["name"]["en"]
        name_fr = pokemon["name"]["fr"]

        # Gérer le champ evolution
        evolution_data = pokemon.get("evolution")
        if evolution_data is None or evolution_data.get("pre") is None:
            evolution = 1  # Si evolution est null -> niveau 1
        else:
            pre_evolutions = evolution_data.get("pre", [])
            evolution = len(pre_evolutions)  # Longueur de la liste des pré-évolutions
            if evolution == 0:
                evolution = 1
            elif evolution == 1:
                evolution = 2
            elif evolution == 2:
                evolution = 3

        # Gérer les types en évitant l'erreur
        types = pokemon.get("types", [])
        type1 = types[0]["name"] if len(types) > 0 and types[0].get("name") else None
        type2 = types[1]["name"] if len(types) > 1 and types[1].get("name") else None

        # Extraire les autres champs
        weight_kg = parse_float(pokemon["weight"])
        height_m = parse_float(pokemon["height"])
        generation = pokemon["generation"]
        classfication = pokemon["category"]

        # Exécuter la requête d'insertion
        cursor.execute(insert_query, (
            pokedex_number, name, name_fr, evolution, type1, type2,
            weight_kg, height_m, generation, classfication
        ))

    print("Données insérées avec succès.")

def main():
    # Connexion à la base de données
    conn = psycopg2.connect(
        dbname=os.getenv("DATABASE_NAME"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host="localhost",
        port="5432"
    )
    try:
        cursor = conn.cursor()

        # Création des tables et insertion des données
        create_tables(cursor)
        insert_pokemon_data(cursor)

        # Valider les changements
        conn.commit()

    except Exception as e:
        print(f"Erreur : {e}")

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
