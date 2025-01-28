from pydantic import BaseModel
from typing import Optional

# Modèle Pydantic pour la table Player
class Player(BaseModel):
    discord_id: str
    player_name: str
    win_count: Optional[int] = None
    win_streak: Optional[int] = None

    class Config:
        from_attributes = True

class PlayerCreate(BaseModel):
    discord_id: str
    player_name: str
    win_count: Optional[int] = None
    win_streak: Optional[int] = None

    class Config:
        from_attributes = True