from fastapi import APIRouter, HTTPException, Depends
from typing import List
import sqlite3
from models import Pokemon, PokemonCreate
from services import get_db_connection, get_pokemon_by_id, create_pokemon

router = APIRouter()

@router.get("/pokemon/{pokedex_number}", response_model=Pokemon)
def read_pokemon(pokedex_number: int, db: sqlite3.Connection = Depends(get_db_connection)):
    result = get_pokemon_by_id(db, pokedex_number)
    if not result:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return Pokemon(**dict(result))

@router.post("/pokemon", status_code=201)
def create_new_pokemon(pokemon: PokemonCreate, db: sqlite3.Connection = Depends(get_db_connection)):
    create_pokemon(db, pokemon)
    return {"message": "Pokémon created successfully"}
