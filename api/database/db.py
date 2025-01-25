import sqlite3

DB_PATH = "database/bot.db"  # Chemin vers la base de données SQLite

def initialize_database():
    """Initialise les tables de la base de données."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Table des utilisateurs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            discord_id INTEGER PRIMARY KEY,                     -- ID unique de l'utilisateur
            username TEXT NOT NULL,                             -- Nom d'utilisateur Discord
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP      -- Date d'inscription
        )
        """)

        # Table des cartes Pokémon
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,    -- ID unique de la carte
            name TEXT NOT NULL,                      -- Nom de la carte
            extension TEXT,                          -- Extension ou set de la carte
            rarity TEXT,                             -- Rareté de la carte
            image_url TEXT                           -- URL ou chemin de l'image de la carte
        )
        """)

        # Table des cartes associées aux utilisateurs (proposées ou recherchées)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,                                   -- ID unique pour chaque entrée
            user_id INTEGER NOT NULL,                                               -- Référence à l'utilisateur (table `users`)
            card_id INTEGER NOT NULL,                                               -- Référence à la carte (table `cards`)
            is_offer BOOLEAN NOT NULL,                                              -- TRUE = carte proposée, FALSE = carte recherchée
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                         -- Date d'enregistrement
            UNIQUE (user_id, card_id, is_offer),                                    -- Empêche les doublons (une carte spécifique pour un utilisateur)
            FOREIGN KEY (user_id) REFERENCES users(discord_id) ON DELETE CASCADE,
            FOREIGN KEY (card_id) REFERENCES cards(id) ON DELETE CASCADE
        )
        """)

        conn.commit()
        print("Base de données initialisée avec succès.")

if __name__ == "__main__":
    initialize_database()
