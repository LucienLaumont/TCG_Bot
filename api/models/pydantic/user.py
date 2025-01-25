from pydantic import BaseModel

class UserCreate(BaseModel):
    id: int
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True