import sqlite3

def get_db_connection():
    connection = sqlite3.connect("database/pokemon.db")
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()

def get_pokemon_by_id(db, pokedex_number: int):
    query = "SELECT * FROM pokemon WHERE pokedex_number = ?"
    result = db.execute(query, (pokedex_number,)).fetchone()
    return result

def create_pokemon(db, pokemon):
    query = """
    INSERT INTO pokemon (name, name_fr, type1, type2, weight_kg, height_m, generation, is_legendary, classfication)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    db.execute(query, (pokemon.name, pokemon.name_fr, pokemon.type1, pokemon.type2,
                       pokemon.weight_kg, pokemon.height_m, pokemon.generation,
                       pokemon.is_legendary, pokemon.classification))
    db.commit()
