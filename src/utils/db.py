
import sqlite3
import os
from pathlib import Path

DB_PATH = Path("output/asana_simulation.sqlite")
SCHEMA_PATH = Path("schema.sql")

def get_connection(db_path=DB_PATH):
    """Creates a connection to the SQLite database."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DB_PATH, schema_path=SCHEMA_PATH):
    """Initializes the database using the schema file."""
    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at {schema_path}")
    
    conn = get_connection(db_path)
    with open(schema_path, "r") as f:
        schema = f.read()
    
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

def wipe_db(db_path=DB_PATH):
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database at {db_path}")