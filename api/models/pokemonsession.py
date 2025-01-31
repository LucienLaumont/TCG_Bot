from sqlalchemy import Column, Integer, String, Float, ForeignKey
from ..services.db import Base

class PokemonSession(Base):
    __tablename__ = "pokemonsession"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(String, ForeignKey("player.discord_id"), nullable=False)
    pokedex_number = Column(Integer, ForeignKey("pokemon.pokedex_number"), nullable=False)
    found = Column(Integer)
    name = Column(String)
    name_fr = Column(String)
    evolution = Column(Integer)
    type1 = Column(String)
    type2 = Column(String)
    weight_kg = Column(String)
    height_m = Column(String)
    generation = Column(Integer)
    classfication = Column(String)