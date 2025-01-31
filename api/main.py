from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text
from .services.db import get_db

from .routes import pokemon, player, pokemonsession

app = FastAPI()

# Inclure les routes Pokémon
app.include_router(pokemon.router, prefix="/api", tags=["pokemon"])
app.include_router(player.router, prefix="/api", tags=["player"])
app.include_router(pokemonsession.router, prefix="/api", tags=["pokemonsession"])


# Route de vérification de la connexion API et base de données
@app.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        # Vérifier si la connexion à la base est établie
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "API et base de données fonctionnent correctement"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": f"Erreur de connexion à la base de données : {str(e)}"}
