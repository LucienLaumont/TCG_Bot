from fastapi import APIRouter, HTTPException, Depends
from services import get_db_connection, get_pokemon_by_id
from utils.utils import compare_pokemon
import random
import uuid

router = APIRouter()

# Sessions de jeu en mémoire
active_sessions = {}

@router.post("/pokedl/start")
def start_game(db=Depends(get_db_connection)):
    # Sélectionner un Pokémon aléatoire
    query = "SELECT * FROM pokemon ORDER BY RANDOM() LIMIT 1"
    target_pokemon = db.execute(query).fetchone()
    if not target_pokemon:
        raise HTTPException(status_code=500, detail="No Pokémon available to start the game.")
    
    # Créer une session de jeu
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = dict(target_pokemon)
    
    return {"session_id": session_id, "message": "New game started. Try to guess the Pokémon!"}

@router.post("/pokedl/guess")
def guess_pokemon(session_id: str, pokedex_number: int, db=Depends(get_db_connection)):
    # Vérifier si la session est active
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    target_pokemon = active_sessions[session_id]
    
    # Récupérer le Pokémon deviné
    guessed_pokemon = get_pokemon_by_id(db, pokedex_number)
    if not guessed_pokemon:
        raise HTTPException(status_code=404, detail="Guessed Pokémon not found.")
    
    # Comparer les Pokémon
    shared_attributes = compare_pokemon(target_pokemon, dict(guessed_pokemon))
    
    if target_pokemon["pokedex_number"] == guessed_pokemon["pokedex_number"]:
        return {"correct": True, "message": f"Congratulations! You've guessed the Pokémon: {target_pokemon['name']}."}
    else:
        return {"correct": False, "shared_attributes": shared_attributes}
