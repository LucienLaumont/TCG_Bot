from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy import select
from typing import List
from fastapi import HTTPException

from urllib.parse import unquote
from unidecode import unidecode

from ..models.pokemon import PokemonModel
from ..models.schemas import PokemonCreate



# Récupérer un Pokémon par son pokedex_number
def get_pokemon_by_id(db: Session, pokedex_number: int):
    return db.query(PokemonModel).filter(PokemonModel.pokedex_number == pokedex_number).first()

def search_pokemon_by_name(db: Session, name: str):
    
    # Décoder l’URL si elle contient des caractères encodés
    decoded_name = unquote(name)

    # Rechercher le Pokémon sans appliquer unidecode sur les colonnes SQL
    pokemon = (
        db.query(PokemonModel)
        .filter(
            (PokemonModel.name.ilike(f"%{decoded_name}%")) |
            (PokemonModel.name_fr.ilike(f"%{decoded_name}%"))
        )
        .first()
    )

    return pokemon

# Ajouter un Pokémon dans la base de données
def create_pokemon(db: Session, pokemon: PokemonCreate):
    db_pokemon = PokemonModel(**pokemon.model_dump())
    try:
        db.add(db_pokemon)
        db.commit()
        db.refresh(db_pokemon)
        return db_pokemon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de l'ajout du Pokémon: {str(e)}")

# Mettre à jour les informations d'un Pokémon existant
def update_pokemon(db: Session, pokedex_number: int, pokemon: PokemonCreate):
    db_pokemon = db.query(PokemonModel).filter(PokemonModel.pokedex_number == pokedex_number).first()
    if not db_pokemon:
        return None

    for key, value in pokemon.model_dump().items():
        setattr(db_pokemon, key, value)

    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon

# Supprimer un Pokémon de la base de données
def delete_pokemon(db: Session, pokedex_number: int):
    db_pokemon = db.query(PokemonModel).filter(PokemonModel.pokedex_number == pokedex_number).first()
    if not db_pokemon:
        return False

    db.delete(db_pokemon)
    db.commit()
    return True

def suggest_pokemon(db: Session, query: str) -> List[str]:
    # Requête pour rechercher les noms de Pokémon similaires
    result = db.execute(
        select(PokemonModel.name_fr)
        .where(PokemonModel.name_fr.ilike(f"%{query}%"))
        .limit(10)
    )

    # Extraire les noms de Pokémon de la réponse
    suggestions = [row[0] for row in result.fetchall()]
    return suggestions