from sqlalchemy.orm import Session
from api.models.card import Card
from api.models.pydantic.card import CardCreate

def create_card_service(db: Session, card_data: CardCreate):

    db_card = db.query(Card).filter(Card.id == card_data.id).first()

    if db_card:
        raise ValueError("Card already exists")
    
    new_card = Card(
        name=card_data.name,
        extension=card_data.extension,
        rarity=card_data.rarity,
        image=card_data.image
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)

    return new_card

def get_card_service(db: Session, card_id: int):
    
    return db.query(Card).filter(Card.id == card_id).first()

def delete_card_service(db: Session, card_id: int):
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise ValueError("Card not found")
    db.delete(card)
    db.commit()