from sqlalchemy.orm import Session
from api.models.user import User
from api.models.card import Card
from api.models.user_cards import user_cards
from api.models.pydantic.user import UserCreate
from api.models.pydantic.user_cards import UserCardsResponse, UserCardLink

def create_user_service(db: Session, user_data: UserCreate):

    db_user = db.query(User).filter(User.id == user_data.id).first()
    
    if db_user:
        raise ValueError("User already exists")
    
    new_user = User(
        id=user_data.id, 
        username=user_data.username
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user_service(db: Session, user_id: int):

    return db.query(User).filter(User.id == user_id).first()

def delete_user_service(db: Session, user_id: int):
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    db.delete(user)
    db.commit()

def get_user_cards_service(db: Session, user_id: int, is_offer: bool):
    """
    Récupère les cartes d'un utilisateur selon `is_offer`.
    - is_offer=True : Cartes offertes.
    - is_offer=False : Cartes recherchées.
    """
    # Récupérer l'utilisateur
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return UserCardsResponse(id=user_id, username="", cards=[])

    # Récupérer les cartes filtrées par `is_offer`
    user_cards_query = (
        db.query(Card, user_cards.c.is_offer)
        .join(user_cards, Card.id == user_cards.c.card_id)
        .filter(user_cards.c.user_id == user_id, user_cards.c.is_offer == is_offer)
        .all()
    )

    # Construire la réponse Pydantic
    cards = [
        UserCardLink(card_id=card.id, is_offer=is_offer)
        for card, is_offer in user_cards_query
    ]

    return UserCardsResponse(
        id=user.id,
        username=user.username,
        cards=cards
    )
