from typing import List, Optional
from sqlalchemy.orm import Session
from api.models.player import Player, PlayerCreate
from api.database.database import get_db, Player as PlayerDBModel

def get_players(db: Session) -> List[Player]:
    return db.query(PlayerDBModel).all()

def get_player_by_discord_id(db: Session, discord_id: str) -> Optional[Player]:
    return db.query(PlayerDBModel).filter(PlayerDBModel.discord_id == discord_id).first()

def create_player(db: Session, player: PlayerCreate) -> Player:
    db_player = PlayerDBModel(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def reset_win_streak(db: Session, discord_id: str):
    # Rechercher le joueur
    player = db.query(Player).filter(Player.discord_id == discord_id).first()
    if not player:
        raise Exception("Player not found")

    # Mettre le win_streak à 0
    player.win_streak = 0
    db.commit()
    db.refresh(player)
    return player