from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./pokemon.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    discord_id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, nullable=False)
    win_count = Column(Integer, nullable=True)
    win_streak = Column(Integer, nullable=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
