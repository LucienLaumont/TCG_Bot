from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.base import Base
from api.models.user import User
from api.models.card import Card
from api.models.user_cards import user_cards
from api.models.pydantic.user import UserCreate
from api.models.pydantic.card import CardCreate

# Fonction pour initialiser la base de données
def init_db():
    engine = create_engine('sqlite:///db.sqlite3')  # Remplacer par l'URL de ta base de données si nécessaire
    Base.metadata.create_all(engine)
    return engine

# Fonction pour ajouter des données à la base de données
def seed_db(session):
    # Ajouter des utilisateurs via UserCreate
    user1_data = UserCreate(id=123456789, username='Ash')
    user2_data = UserCreate(id=987654321, username='Misty')

    user1 = User(id=user1_data.id, username=user1_data.username)
    user2 = User(id=user2_data.id, username=user2_data.username)

    session.add(user1)
    session.add(user2)

    # Ajouter des cartes via CardCreate
    card1_data = CardCreate(name='Pikachu', extension='Base Set', rarity='Rare', image='https://example.com/pikachu.jpg')
    card2_data = CardCreate(name='Bulbasaur', extension='Jungle', rarity='Common', image='https://example.com/bulbasaur.jpg')
    card3_data = CardCreate(name='Charizard', extension='Base Set', rarity='Ultra Rare', image='https://example.com/charizard.jpg')

    card1 = Card(name=card1_data.name, extension=card1_data.extension, rarity=card1_data.rarity, image=card1_data.image)
    card2 = Card(name=card2_data.name, extension=card2_data.extension, rarity=card2_data.rarity, image=card2_data.image)
    card3 = Card(name=card3_data.name, extension=card3_data.extension, rarity=card3_data.rarity, image=card3_data.image)

    session.add(card1)
    session.add(card2)
    session.add(card3)
    session.commit()  # Commit pour sauvegarder les utilisateurs et cartes

    # Associer les utilisateurs avec leurs cartes et is_offer
    session.execute(user_cards.insert().values(user_id=user1.id, card_id=card1.id, is_offer=True))
    session.execute(user_cards.insert().values(user_id=user1.id, card_id=card2.id, is_offer=False))
    session.execute(user_cards.insert().values(user_id=user2.id, card_id=card3.id, is_offer=True))

    # Commit des changements
    session.commit()

if __name__ == '__main__':
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Peupler la base de données
    seed_db(session)
    print("Base de données initialisée avec succès !")
