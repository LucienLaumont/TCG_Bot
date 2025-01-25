from pydantic import BaseModel
from typing import List

class UserCardLink(BaseModel):
    card_id: int
    is_offer: bool

class UserCardsResponse(BaseModel):
    id: int
    username: str
    cards: List[UserCardLink]

    class Config:
        from_attributes = True