from pydantic import BaseModel
from typing import List, Optional

class Pokemon(BaseModel):
    pokedex_number: int
    name: str
    name_fr: str
    evolution: Optional[int] = None
    type1: str
    type2: Optional[str] = None
    weight_kg: float
    height_m: float
    generation: int
    is_legendary: int
    classification: Optional[str] = None

class PokemonCreate(BaseModel):
    name: str
    name_fr: str
    evolution: Optional[int] = None
    type1: str
    type2: Optional[str] = None
    weight_kg: float
    height_m: float
    generation: int
    is_legendary: int
    classification: Optional[str] = None
