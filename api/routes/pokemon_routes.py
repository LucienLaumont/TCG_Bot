from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.models.pokemon import Pokemon, PokemonCreate
from api.services.pokemon_service import get_pokemons, get_pokemon_by_id, create_pokemon
from api.database.database import get_db

router = APIRouter()

@router.get("/pokemon", response_model=List[Pokemon])
def list_pokemons(db: Session = Depends(get_db)):
    return get_pokemons(db)

@router.get("/pokemon/{pokedex_number}", response_model=Pokemon)
def get_pokemon(pokedex_number: int, db: Session = Depends(get_db)):
    pokemon = get_pokemon_by_id(db, pokedex_number)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon

@router.post("/pokemon", response_model=Pokemon)
def add_pokemon(player: PokemonCreate, db: Session = Depends(get_db)):
    return create_pokemon(db, player)
