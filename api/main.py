from fastapi import FastAPI
from api.routers import users, cards

app = FastAPI(title="TCG Bot API", version="1.0")

# Enregistrer les routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(cards.router, prefix="/cards", tags=["Cards"])

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "API is running"}
