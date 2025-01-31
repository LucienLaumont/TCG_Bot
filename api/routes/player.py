from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..models.schemas import Player as PlayerSchema, PlayerCreate
from ..services.player import create_player, get_player_by_id, update_player, delete_player
from ..services.db import get_db

router = APIRouter()

# Créer un joueur
@router.post("/player/", response_model=PlayerSchema)
def add_player(player: PlayerCreate, db: Session = Depends(get_db)):
    db_player = create_player(db, player)
    if not db_player:
        raise HTTPException(status_code=400, detail="Impossible de créer le joueur")
    return db_player

# Récupérer les informations d'un joueur par son discord_id
@router.get("/player/{discord_id}", response_model=PlayerSchema)
def get_player(discord_id: str, db: Session = Depends(get_db)):
    db_player = get_player_by_id(db, discord_id)
    if not db_player:
        raise HTTPException(status_code=404, detail="Le joueur spécifié est introuvable")
    return db_player

# Mettre à jour les informations d'un joueur
@router.put("/player/{discord_id}", response_model=PlayerSchema)
def modify_player(discord_id: str, player: PlayerCreate, db: Session = Depends(get_db)):
    updated_player = update_player(db, discord_id, player)
    if not updated_player:
        raise HTTPException(status_code=404, detail="Le joueur spécifié est introuvable")
    return updated_player

# Supprimer un joueur
@router.delete("/player/{discord_id}")
def remove_player(discord_id: str, db: Session = Depends(get_db)):
    if not delete_player(db, discord_id):
        raise HTTPException(status_code=404, detail="Le joueur spécifié est introuvable")
    return {"detail": "Le joueur a été supprimé avec succès"}
