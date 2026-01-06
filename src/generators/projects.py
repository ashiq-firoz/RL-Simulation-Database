
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date, get_weighted_choice
from datetime import datetime, timedelta
import random

PROJECT_TEMPLATES = {
    "Engineering": ["Q{q} Roadmap", "Bug Tracking", "Infra Migration", "API V{v}", "Security Audit"],
    "Product": ["User Research", "Feature Prioritization", "Launch Plan - {month}", "Competitor Analysis"],
    "Marketing": ["Social Media Calendar", "Q{q} Brand Campaign", "SEO Optimization", "Event: {event}"],
    "Sales": ["Sales Pipeline", "Key Accounts", "Lead Gen Q{q}"],
    "Operations": ["Office Move", "Employee Onboarding", "Monthly Finance Close", "Vendor Selection"]
}

EVENTS = ["TechCrunch Disrupt", "AWS re:Invent", "Quarterly Offsite", "Hackathon"]

def generate_projects(conn, teams_data):
    print("Generating projects...")
    cursor = conn.cursor()
    
    projects_batch = []
    sections_batch = [] # Generate default sections for each project
    
    for team_id, dept in teams_data:
        # 5-20 projects per team
        num_projects = random.randint(5, 20)
        
        # Get team members for ownership
        cursor.execute("SELECT user_id FROM team_memberships WHERE team_id = ?", (team_id,))
        members = [r[0] for r in cursor.fetchall()]
        if not members: continue
        
        for _ in range(num_projects):
            p_id = generate_uuid()
            owner_id = random.choice(members)
            
            # Generate Name
            base_name = random.choice(PROJECT_TEMPLATES.get(dept, PROJECT_TEMPLATES["Operations"]))
            name = base_name.format(
                q=random.randint(1,4), 
                v=random.randint(1,5), 
                month=random.choice(["Jan", "Feb", "Mar"]), 
                event=random.choice(EVENTS)
            )
            
            created_at = datetime.now() - timedelta(days=random.randint(0, 700))
            due_date = created_at + timedelta(days=random.randint(30, 180))
            status = get_weighted_choice(
                ['on_track', 'at_risk', 'off_track', 'on_hold', 'completed'],
                [0.5, 0.2, 0.1, 0.05, 0.15]
            )
            
            projects_batch.append((
                p_id, team_id, owner_id, name, "Generated Project", status, due_date, created_at, 0
            ))
            
            # Default Sections
            for idx, sec_name in enumerate(["To Do", "In Progress", "Review", "Done"]):
                sections_batch.append((generate_uuid(), p_id, sec_name, idx))
            
            if len(projects_batch) >= 500:
                cursor.executemany("""
                    INSERT INTO projects (project_id, team_id, owner_id, name, description, status, due_date, created_at, archived)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, projects_batch)
                
                cursor.executemany("""
                    INSERT INTO sections (section_id, project_id, name, order_index)
                    VALUES (?, ?, ?, ?)
                """, sections_batch)
                
                conn.commit()
                projects_batch = []
                sections_batch = []

    # Final flush
    if projects_batch:
        cursor.executemany("INSERT INTO projects (project_id, team_id, owner_id, name, description, status, due_date, created_at, archived) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", projects_batch)
        cursor.executemany("INSERT INTO sections (section_id, project_id, name, order_index) VALUES (?, ?, ?, ?)", sections_batch)
        conn.commit()
        
    print("Projects generation complete.")