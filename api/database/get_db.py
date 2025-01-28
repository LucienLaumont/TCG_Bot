import sqlite3

def get_db_connection():
    connection = sqlite3.connect("database/pokemon.db")
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()