from pydantic import BaseModel
from typing import List, Optional

# Modèle Pydantic pour représenter une session existante
class PokemonSession(BaseModel):
    id: int
    discord_id: str
    pokedex_number: int
    found: Optional[int] = None
    name: Optional[str] = None
    name_fr: Optional[str] = None
    evolution: Optional[int] = None
    type1: Optional[str] = None
    type2: Optional[str] = None
    weight_kg: Optional[float] = None
    height_m: Optional[float] = None
    generation: Optional[int] = None
    is_legendary: Optional[int] = None
    classfication: Optional[str] = None

    class Config:
        from_attributes = True


# Modèle Pydantic pour créer une nouvelle session
class PokemonSessionCreate(BaseModel):
    discord_id: str
    pokedex_number: int
    found: Optional[int] = None
    name: Optional[str] = None
    name_fr: Optional[str] = None
    evolution: Optional[int] = None
    type1: Optional[str] = None
    type2: Optional[str] = None
    weight_kg: Optional[float] = None
    height_m: Optional[float] = None
    generation: Optional[int] = None
    is_legendary: Optional[int] = None
    classfication: Optional[str] = None

    class Config:
        from_attributes = True