from fastapi import FastAPI
from api.routes import player_routes
from api.database.database import Base, engine

app = FastAPI()

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

# Inclure les routes des joueurs
app.include_router(player_routes.router, prefix="/api", tags=["players"])

@app.get("/")
def root():
    return {"message": "Welcome to the Pokemon API!"}
