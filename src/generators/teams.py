
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
from datetime import datetime, timedelta
import random

CORE_TEAMS = {
    "Engineering": ["Platform", "Core", "Mobile", "Frontend", "Data", "SRE", "Security"],
    "Product": ["Growth", "Enterprise", "Consumer", "Mobile"],
    "Marketing": ["Brand", "Performance", "Content", "Events"],
    "Sales": ["North America", "EMEA", "APAC", "Enterprise Sales"],
    "Operations": ["HR", "Finance", "Legal", "IT"]
}

def generate_teams(conn, workspace_id):
    print("Generating teams...")
    cursor = conn.cursor()
    
    generated_teams = []
    
    # Fetch workspace creation time to ensure teams are created after
    cursor.execute("SELECT created_at FROM workspaces WHERE workspace_id = ?", (workspace_id,))
    ws_created_at = datetime.fromisoformat(cursor.fetchone()[0])

    for dept, subteams in CORE_TEAMS.items():
        for sub in subteams:
            team_id = generate_uuid()
            name = f"{dept} - {sub}"
            desc = f"Official team for {sub} activities within {dept}."
            created_at = ws_created_at + timedelta(days=random.randint(0, 30))
            
            cursor.execute("""
                INSERT INTO teams (team_id, workspace_id, name, description, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (team_id, workspace_id, name, desc, created_at))
            
            generated_teams.append((team_id, dept)) # Store dept for user mapping
            
    conn.commit()
    print(f"Generated {len(generated_teams)} teams.")
    return generated_teams

def assign_memberships(conn, teams_list):
    print("Assigning users to teams...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, job_title, created_at FROM users")
    users = cursor.fetchall()
    
    memberships = []
    
    for user in users:
        u_id = user['user_id']
        title = user['job_title']
        joined_at = datetime.fromisoformat(user['created_at'])
        
        # Simple heuristic mapping
        target_dept = "Operations" # Default
        if "Engineer" in title or "Developer" in title: target_dept = "Engineering"
        elif "Product" in title or "Designer" in title: target_dept = "Product"
        elif "Marketing" in title or "Writer" in title or "SEO" in title: target_dept = "Marketing"
        elif "Sales" in title or "Account" in title: target_dept = "Sales"
        
        # Find matching teams
        dept_teams = [t[0] for t in teams_list if t[1] == target_dept]
        if not dept_teams:
            dept_teams = [t[0] for t in teams_list] # Fallback
            
        # Assign to 1-3 teams
        num_teams = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05])[0]
        selected_teams = random.sample(dept_teams, k=min(len(dept_teams), num_teams))
        
        for t_id in selected_teams:
            role = 'admin' if 'Manager' in title or 'Director' in title else 'member'
            memberships.append((t_id, u_id, role, joined_at))
            
        if len(memberships) >= 1000:
            cursor.executemany("INSERT INTO team_memberships (team_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)", memberships)
            conn.commit()
            memberships = []
            
    if memberships:
        cursor.executemany("INSERT INTO team_memberships (team_id, user_id, role, joined_at) VALUES (?, ?, ?, ?)", memberships)
        conn.commit()
        
    print("Team membership assignment complete.")
