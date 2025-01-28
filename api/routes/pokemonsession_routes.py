from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.models.pokemonsession import PokemonSession, PokemonSessionCreate
from api.services.player_service import reset_win_streak
from api.services.pokemonsession_service import get_pokemonsessions, get_pokemonsession_by_id, create_pokemonsession,delete_pokemonsession
from api.database import database

router = APIRouter()

@router.get("/pokemonsession", response_model=List[PokemonSession])
def list_pokemonsessions(db: Session = Depends(database.get_db)):
    return get_pokemonsessions(db)

@router.get("/pokemonsession/{pokemonsession_id}", response_model=PokemonSession)
def get_pokemonsession(session_id: int, db: Session = Depends(database.get_db)):
    session = get_pokemonsession_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.post("/pokemonsession", response_model=PokemonSession)
def add_pokemonsession(session: PokemonSessionCreate, db: Session = Depends(database.get_db)):
    # Vérifier si le joueur existe
    player = db.query(database.Player).filter(database.Player.discord_id == session.discord_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player with the given Discord ID does not exist")

    # Vérifier si le Pokémon existe
    pokemon = db.query(database.Pokemon).filter(database.Pokemon.pokedex_number == session.pokedex_number).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon with the given Pokedex number does not exist")

    # Vérifier si le joueur a déjà une session active
    active_session = db.query(database.PokemonSession).filter(database.PokemonSession.discord_id == session.discord_id).first()
    if active_session:
        print("Delete Previous Pokemonsession")
        delete_pokemonsession(db, active_session)
        reset_win_streak(db, session.discord_id)

    # Créer une nouvelle session Pokémon
    print("Create New Pokemonsession")
    new_session = create_pokemonsession(db, session)
    return new_session

@router.delete("/pokemonsession/{discord_id}", status_code=204)
def del_pokemonsession(discord_id: str, db: Session = Depends(database.get_db)):
    # Vérifier si une session existe pour le joueur
    active_session = db.query(database.PokemonSession).filter(database.PokemonSession.discord_id == discord_id).first()
    if not active_session:
        raise HTTPException(status_code=404, detail="No active session found for the given player")
    else:
        delete_pokemonsession(db, active_session)