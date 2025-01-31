from sqlalchemy.orm import Session
from ..models.schemas import PokemonSessionCreate
from ..models.pokemonsession import PokemonSession as PokemonSessionModel
from ..models.player import PlayerModel
from ..models.pokemon import PokemonModel

# Récupérer toutes les sessions
def get_pokemonsessions(db: Session):
    return db.query(PokemonSessionModel).all()

# Récupérer une session par ID
def get_pokemonsession_by_id(db: Session, session_id: int):
    return db.query(PokemonSessionModel).filter(PokemonSessionModel.id == session_id).first()

# Récupérer la session d'un utilisateur
def get_player_pokemonsession(db: Session, discord_id: str):
    return db.query(PokemonSessionModel).filter(PokemonSessionModel.discord_id == discord_id).first()

# Créer une nouvelle session Pokémon
def create_pokemonsession(db: Session, session: PokemonSessionCreate):
    new_session = PokemonSessionModel(**session.dict())
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return new_session

# Modifier la session d'un joueur
def update_pokemonsession_with_guess(db: Session, discord_id: str, guessed_pokemon: dict):

    # Récupérer la session active du joueur
    session = db.query(PokemonSessionModel).filter(PokemonSessionModel.discord_id == discord_id).first()

    if not session:
        print(f"Aucune session trouvée pour l'utilisateur {discord_id}.")
        return None

    correct_fields = [
        "name", "name_fr", "type1", "type2", "evolution", "weight_kg", "height_m", "generation", "classfication", "is_legendary"
    ]

    # Comparer et mettre à jour les champs corrects dans la session
    for field in correct_fields:
        guessed_value = guessed_pokemon['guessed_pokemon'].get(field)
        setattr(session, field, guessed_value)

    # Sauvegarder les changements dans la base de données
    db.commit()
    db.refresh(session)

    return session

# Supprimer une session Pokémon existante
def delete_pokemonsession(db: Session, session: PokemonSessionModel):
    db.delete(session)
    db.commit()

# Réinitialiser le win streak d'un joueur
def reset_win_streak(db: Session, discord_id: str):
    player = db.query(PlayerModel).filter(PlayerModel.discord_id == discord_id).first()
    if player:
        player.win_streak = 0
        db.commit()