import sqlite3 
from pathlib import Path

db_path=Path('db/fitness_app.db')
schema_path=Path('db/schema.sql')

def init_db():
    conn=sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys= ON;")

    with open(schema_path,'r', encoding='utf-8') as db:
        schema=db.read()
    conn.executescript(schema)

    conn.commit()
    conn.close()
    print(f"Database successfully created at {db_path.resolve()}")

if __name__=="__main__":
    init_db()