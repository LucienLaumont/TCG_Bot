import os
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.models.user import User

from api.config import DEV_MODE

def get_current_user_id(ctx: Request) -> int:
    """
    Récupère l'ID Discord de l'utilisateur actuel depuis le contexte.
    En mode développement, retourne un ID par défaut si le contexte est manquant.
    """
    if DEV_MODE:
        print("[DEV_MODE] get_current_user_id called")
        return 123456789  # ID fictif pour le mode développement

    try:
        author = getattr(ctx, "author", None)
        user_id = getattr(author, "id", None)
        if not user_id:
            raise ValueError("User ID not found in context")
        return user_id
    except AttributeError:
        raise HTTPException(status_code=400, detail="Invalid request context or missing user ID")

def get_current_user(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
) -> User:
    """
    Récupère l'utilisateur actuel à partir de la base de données.
    Utilise l'ID Discord comme clé pour effectuer la recherche.
    En mode développement, retourne un utilisateur fictif si aucun utilisateur n'est trouvé.
    """
    if DEV_MODE:
        print("[DEV_MODE] get_current_user called")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            print(f"[DEV_MODE] Creating fake user with ID {user_id}")
            user = User(id=user_id, username="TestUser")
            db.add(user)
            db.commit()
        return user

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
