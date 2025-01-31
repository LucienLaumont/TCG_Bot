from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from unidecode import unidecode

from ..models.schemas import Pokemon as PokemonSchema, PokemonCreate
from ..services.pokemon import create_pokemon, update_pokemon, delete_pokemon, get_pokemon_by_id, search_pokemon_by_name
from ..services.db import get_db

router = APIRouter()

# Récupérer un Pokémon par son pokedex_number
@router.get("/pokemon/{pokedex_number}", response_model=PokemonSchema)
def get_pokemon(pokedex_number: int, db: Session = Depends(get_db)):
    db_pokemon = get_pokemon_by_id(db, pokedex_number)
    if not db_pokemon:
        raise HTTPException(status_code=404, detail="Le Pokémon spécifié est introuvable")
    return db_pokemon

@router.get("/pokemon/search/")
def search_pokemon(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):

    pokemon = search_pokemon_by_name(db, name)

    if not pokemon:
        raise HTTPException(status_code=404, detail="Aucun Pokémon trouvé avec ce nom.")

    return {
        "pokedex_number": pokemon.pokedex_number,
        "name": pokemon.name,
        "name_fr": pokemon.name_fr,
        "type1": pokemon.type1,
        "type2": pokemon.type2,
        "evolution": pokemon.evolution,
        "weight_kg": pokemon.weight_kg,
        "height_m": pokemon.height_m,
        "generation": pokemon.generation,
        "classfication": pokemon.classfication,
        "is_legendary": pokemon.is_legendary
    }

# Ajouter un nouveau Pokémon
@router.post("/pokemon/", response_model=PokemonSchema)
def add_pokemon(pokemon: PokemonCreate, db: Session = Depends(get_db)):
    db_pokemon = create_pokemon(db, pokemon)
    if not db_pokemon:
        raise HTTPException(status_code=400, detail="Impossible d'ajouter le Pokémon")
    return db_pokemon

# Mettre à jour les informations d'un Pokémon
@router.put("/pokemon/{pokedex_number}", response_model=PokemonSchema)
def modify_pokemon(pokedex_number: int, pokemon: PokemonCreate, db: Session = Depends(get_db)):
    updated_pokemon = update_pokemon(db, pokedex_number, pokemon)
    if not updated_pokemon:
        raise HTTPException(status_code=404, detail="Le Pokémon spécifié est introuvable")
    return updated_pokemon

# Supprimer un Pokémon
@router.delete("/pokemon/{pokedex_number}")
def remove_pokemon(pokedex_number: int, db: Session = Depends(get_db)):
    if not delete_pokemon(db, pokedex_number):
        raise HTTPException(status_code=404, detail="Le Pokémon spécifié est introuvable")
    return {"detail": "Le Pokémon a été supprimé avec succès"}
