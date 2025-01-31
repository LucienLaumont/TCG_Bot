from sqlalchemy import Column, Integer, String
from ..services.db import Base

# Modèle SQLAlchemy pour la table "player"
class PlayerModel(Base):
    __tablename__ = "player"

    discord_id = Column(String, primary_key=True, index=True)
    player_name = Column(String, nullable=False)
    win_count = Column(Integer, nullable=True, default=0)
    win_streak = Column(Integer, nullable=True, default=0)