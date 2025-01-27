from fastapi import FastAPI
from api.routes.pokemon_routes import router

app = FastAPI()

# Inclure les routes définies dans routes.py
app.include_router(router)