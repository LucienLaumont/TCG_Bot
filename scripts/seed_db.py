from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.base import Base
from api.models.user import User
from api.models.card import Card
from api.models.user_cards import user_cards

# Fonction pour initialiser la base de données
def init_db():
    engine = create_engine('sqlite:///db.sqlite3')  # Remplacer par l'URL de ta base de données si nécessaire
    Base.metadata.create_all(engine)
    return engine

# Fonction pour ajouter des données à la base de données
def seed_db(session):
    # Ajouter des utilisateurs
    user1 = User(id=123456789, username='Ash')
    user2 = User(id=987654321, username='Misty')

    # Ajouter des cartes
    card1 = Card(name='Pikachu', extension='Base Set', rarity='Rare', image='https://example.com/pikachu.jpg')
    card2 = Card(name='Bulbasaur', extension='Jungle', rarity='Common', image='https://example.com/bulbasaur.jpg')
    card3 = Card(name='Charizard', extension='Base Set', rarity='Ultra Rare', image='https://example.com/charizard.jpg')

    # Ajouter des relations entre utilisateurs et cartes
    session.add(user1)
    session.add(user2)
    session.add(card1)
    session.add(card2)
    session.add(card3)
    session.commit()  # Sauvegarde les utilisateurs et les cartes pour obtenir leurs IDs

    # Ajouter les paramètres is_offer
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
