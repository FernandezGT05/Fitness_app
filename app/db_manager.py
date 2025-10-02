from pathlib import Path
import sqlite3

db_path = Path(__file__).parent.parent / 'db' / 'fitness_app.db'

def get_connection():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
