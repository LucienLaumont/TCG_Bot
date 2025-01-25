from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.services.cards_service import create_card_service, get_card_service,delete_card_service
from api.models.pydantic.card import CardCreate, CardResponse

router = APIRouter()

@router.post("/", response_model=CardResponse)
def create_card(card: CardCreate, db: Session = Depends(get_db)):
    try:
        return create_card_service(db, card)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: int, db: Session = Depends(get_db)):
    try:
        return get_card_service(db, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{card_id}", status_code=204)
def delete_card(card_id: int, db: Session = Depends(get_db)):
    try:
        delete_card_service(db, card_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
