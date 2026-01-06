
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid
from datetime import datetime, timedelta
import pandas as pd

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

    # Load YC Companies
    try:
        df = pd.read_csv("src/scrapers/data/yc_companies.csv")
        company = df.sample(1).iloc[0]
        name = company['company_name']
        domain = company['domain']
    except Exception as e:
        print(f"Warning: Could not load YC data ({e}). Using default.")
        name = "TechFlow Solutions"
        domain = "techflow.io"

    workspace_id = generate_uuid()
    created_at = datetime.now() - timedelta(days=365*5)

    cursor.execute("""
        INSERT INTO workspaces (workspace_id, name, domain, created_at)
        VALUES (?, ?, ?, ?)
    """, (workspace_id, name, domain, created_at))
    
    conn.commit()
    print(f"Generated Workspace: {name} ({workspace_id})")
    return workspace_id,domain
