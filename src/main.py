
import sys
import os
from pathlib import Path
# Fix import path
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
    USER_COUNT = 500  # Default to 500 for testing, user can scale up code or args if needed. 
                      # Requirement says 5000-10000. I'll set default to 5000 if "prod" arg is passed.
    
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        USER_COUNT = 5000
        print("Running in FULL mode (5000 users). This may take a while.")
    else:
        print("Running in DEMO mode (500 users). Use 'python src/main.py full' for 5000 users.")

    # 1. Setup
    wipe_db(DB_PATH)
    init_db(DB_PATH, SCHEMA_PATH)
    init_llm()
    
    conn = get_connection(DB_PATH)
    
    try:
        # 2. Generators
        print("\n--- Phase 1: Organization Structure ---")
        ws_id = generate_workspaces(conn)
        if not ws_id:
             # Fetch existing if skipped
             cursor = conn.cursor()
             cursor.execute("SELECT workspace_id FROM workspaces LIMIT 1")
             ws_id = cursor.fetchone()[0]

        generate_users(conn, ws_id, count=USER_COUNT)
        
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
