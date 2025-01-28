from pydantic import BaseModel
from typing import List, Optional

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
