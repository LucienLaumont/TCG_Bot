from pydantic import BaseModel
from typing import Optional

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

class Pokemon(BaseModel):
    pokedex_number: int
    name: str
    name_fr: str
    evolution: Optional[int] = None
    type1: str
    type2: Optional[str] = None
    weight_kg: Optional[float] = None
    height_m: Optional[float] = None
    generation: int
    is_legendary: int
    classfication: Optional[str] = None

    class Config:
        from_attributes = True

class PokemonCreate(BaseModel):
    name: str
    name_fr: str
    evolution: Optional[int] = None
    type1: str
    type2: Optional[str] = None
    weight_kg: Optional[float] = None
    height_m: Optional[float] = None
    generation: int
    is_legendary: int
    classfication: Optional[str] = None

    class Config:
        from_attributes = True

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