from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./pokemon.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    discord_id = Column(String, primary_key=True, index=True)
    player_name = Column(String, nullable=False)
    win_count = Column(Integer, nullable=True)
    win_streak = Column(Integer, nullable=True)

class Pokemon(Base):
    __tablename__ = "pokemon"
    pokedex_number = Column(Integer, primary_key=True, index=True)  # Identifiant unique
    name = Column(String, nullable=False)  # Nom en anglais
    name_fr = Column(String, nullable=False)  # Nom en français
    evolution = Column(Integer, nullable=True)  # Identifiant de l'évolution
    type1 = Column(String, nullable=False)  # Type principal
    type2 = Column(String, nullable=True)  # Type secondaire
    weight_kg = Column(Float, nullable=True)  # Poids en kilogrammes
    height_m = Column(Float, nullable=True)  # Taille en mètres
    generation = Column(Integer, nullable=False)  # Génération du Pokémon
    is_legendary = Column(Boolean, nullable=False)  # Est-ce un Pokémon légendaire
    classfication = Column(String, nullable=True)  # Classification (ex: "Seed Pokémon")

class PokemonSession(Base):
    __tablename__ = "session"
    id = Column(Integer, primary_key=True, index=True)  # Identifiant unique de la session
    discord_id = Column(String, ForeignKey("player.discord_id", ondelete="CASCADE"), nullable=False)  # Référence à un joueur
    pokedex_number = Column(Integer, ForeignKey("pokemon.pokedex_number", ondelete="CASCADE"), nullable=False)  # Référence à un Pokémon cible
    found = Column(Integer, nullable=True)  # Champ pour indiquer si le Pokémon a été trouvé

    # Champs supplémentaires de la table pokemon
    name = Column(String, nullable=True)  # Nom anglais
    name_fr = Column(String, nullable=True)  # Nom français
    evolution = Column(Integer, nullable=True)  # Référence à l'évolution
    type1 = Column(String, nullable=True)  # Type principal
    type2 = Column(String, nullable=True)  # Type secondaire
    weight_kg = Column(Float, nullable=True)  # Poids en kilogrammes
    height_m = Column(Float, nullable=True)  # Taille en mètres
    generation = Column(Integer, nullable=True)  # Génération du Pokémon
    is_legendary = Column(Integer, nullable=True)  # Est-ce un Pokémon légendaire ?
    classfication = Column(String, nullable=True)  # Classification ou description du Pokémon

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
