from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .user_cards import user_cards

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # ID utilisateur Discord
    username = Column(String, nullable=False)  # Nom d'utilisateur pour référence locale

    # Relation avec les cartes via la table user_cards
    cards = relationship('Card', secondary=user_cards, back_populates='users')
