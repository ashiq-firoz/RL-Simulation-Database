
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.utils.db import init_db, wipe_db, get_connection
from src.utils.llm import init_llm
from src.generators.workspaces import generate_workspaces
from src.generators.users import generate_users
from src.generators.teams import generate_teams, assign_memberships
from src.generators.projects import generate_projects
from src.generators.tasks import generate_tasks
from src.generators.stories import generate_stories
from src.generators.tags import generate_tags
from src.generators.custom_fields import generate_custom_fields

def main():
    print("=== Asana Simulation Data Generator ===")
    
    # Configuration
    DB_PATH = Path("output/asana_simulation.sqlite")
    SCHEMA_PATH = Path("schema.sql")
    USER_COUNT = 5000  
    
    

    # 1. Setup
    wipe_db(DB_PATH)
    init_db(DB_PATH, SCHEMA_PATH)
    init_llm()
    
    conn = get_connection(DB_PATH)
    
    try:
        # 2. Generators
        print("\n--- Phase 1: Organization Structure ---")
        ws_id, domain = generate_workspaces(conn)
        if not ws_id:
             # Fetch existing if skipped
             cursor = conn.cursor()
             cursor.execute("SELECT workspace_id, domain FROM workspaces LIMIT 1")
             row = cursor.fetchone()
             ws_id = row[0]
             domain = row[1] if row else "startup.io"

        generate_users(conn, ws_id, domain=domain, count=USER_COUNT)
        
        teams = generate_teams(conn, ws_id)
        assign_memberships(conn, teams)
        
        print("\n--- Phase 2: Work Management ---")
        generate_projects(conn, teams)
        generate_tags(conn, ws_id)
        generate_custom_fields(conn, ws_id)
        generate_tasks(conn)
        
        print("\n--- Phase 3: Activity ---")
        generate_stories(conn)
        
        print("\n=== Simulation Complete ===")
        print(f"Database available at: {DB_PATH}")
        
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

if __name__ == "__main__":
    main()
