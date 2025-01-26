from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.dependencies import get_current_user
from api.services.users_service import create_user_service, get_user_service, delete_user_service, get_user_cards_service
from api.models.user import User
from api.models.pydantic.user import UserCreate, UserResponse
from api.models.pydantic.user_cards import UserCardsResponse

import logging

logger = logging.getLogger("api")

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user_service(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    print("User obtenue")
    try:
        return get_user_service(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        delete_user_service(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/cards/")
def get_user_cards(
    offer_type: str,
    search_user: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Récupère les cartes d'un utilisateur (courant ou cible) selon le type (offers ou searches).
    """
    print("Declaration passé ! ")
    # Validation du paramètre offer_type
    if offer_type.lower() not in ["offers", "searches"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid offer_type. Must be 'offers' or 'searches'."
        )

    # Détermine si on recherche pour l'utilisateur courant ou un autre utilisateur
    user_id = search_user if search_user else current_user.id
    is_offer = True if offer_type.lower() == "offers" else False

    # Appelle le service pour récupérer les cartes
    return get_user_cards_service(db, user_id, is_offer)