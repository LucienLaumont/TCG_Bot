from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .user_cards import user_cards

class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Nom de la carte
    extension = Column(String, nullable=False)  # Extension de la carte
    rarity = Column(String, nullable=False)  # Rareté de la carte
    image = Column(String, nullable=True)  # URL de l'image de la carte

    # Relation avec les utilisateurs via la table user_cards
    users = relationship('User', secondary=user_cards, back_populates='cards')
