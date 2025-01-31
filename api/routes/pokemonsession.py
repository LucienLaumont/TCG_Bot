from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from ..models.schemas import PokemonSession, PokemonSessionCreate
from ..services.db import get_db
from ..services.pokemonsession import (
    get_pokemonsessions,
    get_pokemonsession_by_id,
    create_pokemonsession,
    delete_pokemonsession,
    reset_win_streak,
    update_pokemonsession_with_guess,
    get_player_pokemonsession
)
from ..models.player import PlayerModel
from ..models.pokemon import PokemonModel
from ..models.pokemonsession import PokemonSession as PokemonSessionModel

router = APIRouter()

# Récupérer la liste de toutes les sessions Pokémon
@router.get("/pokemonsession", response_model=List[PokemonSession])
def list_pokemonsessions(db: Session = Depends(get_db)):
    return get_pokemonsessions(db)

# Récupérer une session Pokémon par ID
@router.get("/pokemonsession/{session_id}", response_model=PokemonSession)
def get_pokemonsession(session_id: int, db: Session = Depends(get_db)):
    session = get_pokemonsession_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/pokemonsession/active/{discord_id}", response_model=PokemonSession)
def get_active_pokemonsession(discord_id: str, db: Session = Depends(get_db)):
    session = get_player_pokemonsession(db, discord_id)
    if not session:
        raise HTTPException(status_code=404, detail="Aucune session active trouvée pour cet utilisateur.")
    return session

# Créer une nouvelle session Pokémon
@router.post("/pokemonsession/", response_model=PokemonSession)
def add_pokemonsession(session: PokemonSessionCreate, db: Session = Depends(get_db)):
    # Vérifier si le joueur existe
    player = db.query(PlayerModel).filter(PlayerModel.discord_id == session.discord_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player with the given Discord ID does not exist")

    # Vérifier si le Pokémon existe
    pokemon = db.query(PokemonModel).filter(PokemonModel.pokedex_number == session.pokedex_number).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon with the given Pokedex number does not exist")

    # Vérifier si le joueur a déjà une session active
    active_session = db.query(PokemonSessionModel).filter(PokemonSessionModel.discord_id == session.discord_id).first()
    if active_session:
        delete_pokemonsession(db, active_session)
        reset_win_streak(db, session.discord_id)

    new_session = create_pokemonsession(db, session)
    return new_session

# Modifier la session active d'un joueur
@router.put("/pokemonsession/update/{discord_id}")
def update_pokemonsession(discord_id: str, guessed_pokemon: dict, db: Session = Depends(get_db)):
    updated_session = update_pokemonsession_with_guess(db, discord_id, guessed_pokemon)

    if not updated_session:
        raise HTTPException(status_code=404, detail="Aucune session active trouvée ou erreur lors de la mise à jour.")

    return updated_session

# Supprimer la session active d'un joueur
@router.delete("/pokemonsession/{discord_id}", status_code=204)
def del_pokemonsession(discord_id: str, db: Session = Depends(get_db)):
    # Vérifier si une session existe pour le joueur
    active_session = db.query(PokemonSessionModel).filter(PokemonSessionModel.discord_id == discord_id).first()
    if not active_session:
        raise HTTPException(status_code=404, detail="No active session found for the given player")
    
    delete_pokemonsession(db, active_session)
