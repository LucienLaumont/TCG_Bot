from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.models.player import Player, PlayerCreate
from api.services.player_service import get_players, get_player_by_discord_id, create_player
from api.database.database import get_db

router = APIRouter()

@router.get("/players", response_model=List[Player])
def list_players(db: Session = Depends(get_db)):
    return get_players(db)

@router.get("/players/{discord_id}", response_model=Player)
def get_player(discord_id: str, db: Session = Depends(get_db)):
    player = get_player_by_discord_id(db, discord_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player

@router.post("/players", response_model=Player)
def add_player(player: PlayerCreate, db: Session = Depends(get_db)):
    return create_player(db, player)
