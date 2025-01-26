from fastapi import FastAPI,Depends
from api.routers import users, cards
from api.models.user import User
from api.dependencies import get_current_user

app = FastAPI(title="TCG Bot API", version="1.0")

# Enregistrer les routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(cards.router, prefix="/cards", tags=["Cards"])


@app.get("/current_user")
def test_dependency(
    current_user: User = Depends(get_current_user)
):
    print("Test route reached")
    return {"message": "Dependency test passed"}

@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "message": "API is running"}
