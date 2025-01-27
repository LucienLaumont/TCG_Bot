from fastapi import FastAPI
from routes import router

app = FastAPI()

# Inclure les routes définies dans routes.py
app.include_router(router)