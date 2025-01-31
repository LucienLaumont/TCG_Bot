from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.player import PlayerModel
from ..models.schemas import PlayerCreate

# Créer un joueur
def create_player(db: Session, player: PlayerCreate):
    db_player = PlayerModel(**player.model_dump())
    try:
        db.add(db_player)
        db.commit()
        db.refresh(db_player)
        return db_player
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création du joueur : {str(e)}")

# Récupérer un joueur par son discord_id
def get_player_by_id(db: Session, discord_id: str):
    return db.query(PlayerModel).filter(PlayerModel.discord_id == discord_id).first()

# Mettre à jour les informations d'un joueur
def update_player(db: Session, discord_id: str, player: PlayerCreate):
    db_player = get_player_by_id(db, discord_id)
    if not db_player:
        return None

    for key, value in player.model_dump().items():
        setattr(db_player, key, value)

    db.commit()
    db.refresh(db_player)
    return db_player

# Supprimer un joueur par son discord_id
def delete_player(db: Session, discord_id: str):
    db_player = get_player_by_id(db, discord_id)
    if not db_player:
        return False

    db.delete(db_player)
    db.commit()
    return True
