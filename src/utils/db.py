import sqlite3
import os
from pathlib import Path

def get_db_connection(db_path: str = "../output/asana_simulation.sqlite"):
    """Creates a connection to the SQLite database."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    # This enables column access by name: row['column_name']
    conn.row_factory = sqlite3.Row 
    return conn

def init_database(schema_path: str = "../schema.sql", db_path: str = "../output/asana_simulation.sqlite"):
    """
    Reads the schema.sql file and executes it to create tables.
    Drops existing data if the file exists to ensure a clean slate.
    """
    print(f"Initializing database at {db_path}...")
    
    # Check if schema exists
    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema file not found at {schema_path}")

    # Read schema
    with open(schema_path, 'r') as f:
        schema_sql = f.read()

    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    try:
        cursor.executescript(schema_sql)
        conn.commit()
        print("Database initialized and tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while initializing the database: {e}")
    finally:
        conn.close()