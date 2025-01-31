from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Float
from ..services.db import Base

# Modèle SQLAlchemy pour la table "pokemon"
class PokemonModel(Base):
    __tablename__ = "pokemon"

    pokedex_number = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    name_fr = Column(String, nullable=False)
    evolution = Column(Integer, nullable=True)
    type1 = Column(String, nullable=False)
    type2 = Column(String, nullable=True)
    weight_kg = Column(Float, nullable=True)
    height_m = Column(Float, nullable=True)
    generation = Column(Integer, nullable=False)
    is_legendary = Column(Integer, nullable=False)
    classfication = Column(String, nullable=True)