from pydantic import BaseModel
from typing import List, Optional

class Pokemon(BaseModel):
    pokedex_number: int
    name: str
    name_fr: str
    type1: str
    type2: Optional[str]
    weight_kg: float
    height_m: float
    generation: int
    is_legendary: int
    classfication: str

class PokemonCreate(BaseModel):
    name: str
    name_fr: str
    type1: str
    type2: Optional[str]
    weight_kg: float
    height_m: float
    generation: int
    is_legendary: int
    classfication: str
