from typing import List, Optional
from sqlalchemy.orm import Session
from api.models.pokemon import Pokemon, PokemonCreate
from api.database.database import get_db, Pokemon as PokemonDBModel

def get_pokemons(db: Session) -> List[Pokemon]:
    return db.query(PokemonDBModel).all()

def get_pokemon_by_id(db: Session, pokedex_number: int) -> Optional[Pokemon]:
    return db.query(PokemonDBModel).filter(PokemonDBModel.pokedex_number == pokedex_number).first()

def create_pokemon(db: Session, pokemon: PokemonCreate) -> Pokemon:
    db_pokemon = PokemonDBModel(**pokemon.model_dump())
    db.add(db_pokemon)
    db.commit()
    db.refresh(db_pokemon)
    return db_pokemon
