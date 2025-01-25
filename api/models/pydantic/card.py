from pydantic import BaseModel


class CardCreate(BaseModel):
    name: str
    extension: str
    rarity: str
    image: str | None = None  

class CardResponse(BaseModel):
    id: int
    name: str
    extension: str
    rarity: str
    image: str | None = None

    class Config:
        from_attributes = True
