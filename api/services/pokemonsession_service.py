from typing import List, Optional
from sqlalchemy.orm import Session
from api.models.pokemonsession import PokemonSession,PokemonSessionCreate
from api.database.database import get_db, PokemonSession as PokemonSessionDBModel

def get_pokemonsessions(db: Session) -> List[PokemonSession]:
    return db.query(PokemonSessionDBModel).all()

def get_pokemonsession_by_id(db: Session, id: int) -> Optional[PokemonSession]:
    return db.query(PokemonSessionDBModel).filter(PokemonSessionDBModel.id == id).first()

def create_pokemonsession(db: Session, pokemonsession: PokemonSessionCreate) -> PokemonSession:

    new_pokemonsession = PokemonSessionDBModel(**pokemonsession.model_dump())
    db.add(new_pokemonsession)
    db.commit()
    db.refresh(new_pokemonsession)

    return new_pokemonsession

def delete_pokemonsession(db: Session, pokemonsession: PokemonSession):
    db.delete(pokemonsession)
    db.commit()