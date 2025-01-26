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

def get_card_by_id_service(db: Session, card_id: int):
    """
    Recherche une carte unique par son ID.
    """
    return db.query(Card).filter(Card.id == card_id).first()

def search_cards_service(
    db: Session,
    name: str,
    extension: str | None = None,
    rarity: str | None = None,
    limit: int = 10,
    offset: int = 0
):
    """
    Recherche des cartes avec des critères multiples.
    - `name` : Nom partiel ou complet de la carte (obligatoire).
    - `extension` : Filtre par extension (optionnel).
    - `rarity` : Filtre par rareté (optionnel).
    - `limit` : Nombre maximum de résultats (par défaut 10).
    - `offset` : Décalage pour la pagination (par défaut 0).
    """
    query = db.query(Card).filter(Card.name.ilike(f"%{name}%"))  # Recherche insensible à la casse

    if extension:
        query = query.filter(Card.extension.ilike(f"%{extension}%"))  # Filtrer par extension

    if rarity:
        query = query.filter(Card.rarity.ilike(f"%{rarity}%"))  # Filtrer par rareté

    return query.offset(offset).limit(limit).all()  # Appliquer pagination et retourner les résultats



def delete_card_service(db: Session, card_id: int):

    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise ValueError("Card not found")
    db.delete(card)
    db.commit()