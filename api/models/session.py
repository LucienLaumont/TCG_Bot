from pydantic import BaseModel
from typing import List, Optional

# Modèle Pydantic pour la table Session
class Session(BaseModel):
    id: int
    player_discord_id: int
    target_pokemon_id: int
    found: Optional[int] = None

class SessionCreate(BaseModel):
    player_discord_id: int
    target_pokemon_id: int
    found: Optional[int] = None