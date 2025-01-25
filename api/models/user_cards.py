from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from .base import Base

user_cards = Table(
    'user_cards', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('card_id', Integer, ForeignKey('cards.id'), primary_key=True),
    Column('is_offer', Boolean, nullable=False)  # True si la carte est offerte, False si recherchée
)
