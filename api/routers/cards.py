from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.services.cards_service import create_card_service, get_card_by_id_service,search_cards_service,delete_card_service
from api.models.pydantic.card import CardCreate, CardResponse

router = APIRouter()

@router.post("/", response_model=CardResponse)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    try:
        return create_card_service(db, card)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[CardResponse])
def search_cards(
    id: int | None = None,
    name: str = Query(..., description="Name of the card to search"),
    extension: str | None = Query(None, description="Extension of the card"),
    rarity: str | None = Query(None, description="Rarity of the card"),
    limit: int = Query(10, description="Maximum number of results to return"),
    offset: int = Query(0, description="Offset for pagination"),
    db: Session = Depends(get_db),
):
    if id:
        card = get_card_by_id_service(db, id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found with the given ID")
        return [card]  # Retourne une liste contenant une seule carte

    cards = search_cards_service(db, name, extension, rarity, limit, offset)
    if not cards:
        raise HTTPException(status_code=404, detail="No cards found with the given criteria")
    return cards


@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    try:
        delete_card_service(db, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
