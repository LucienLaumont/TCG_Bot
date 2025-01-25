from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.config import DATABASE_URL

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Sessionmaker pour les interactions avec la base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dépendance pour les endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
