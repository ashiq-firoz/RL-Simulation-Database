
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid
from datetime import datetime, timedelta

def generate_workspaces(conn):
    """
    Generates the primary workspace for the simulation.
    """
    cursor = conn.cursor()
    
    # Check if workspace already exists
    cursor.execute("SELECT count(*) FROM workspaces")
    if cursor.fetchone()[0] > 0:
        print("Workspaces already exist. Skipping.")
        return

    # Simulation: A B2B SaaS Company
    workspace_id = generate_uuid()
    name = "TechFlow Solutions"
    domain = "techflow.io"
    created_at = datetime.now() - timedelta(days=365*5) # 5 years old

    cursor.execute("""
        INSERT INTO workspaces (workspace_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
    """, (workspace_id, name, domain, created_at))
    
    conn.commit()
    print(f"Generated Workspace: {name} ({workspace_id})")
    return workspace_id
