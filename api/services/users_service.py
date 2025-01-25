from sqlalchemy.orm import Session
from api.models.user import User
from api.models.pydantic.user import UserCreate

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