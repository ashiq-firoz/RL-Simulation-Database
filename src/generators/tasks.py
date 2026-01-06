
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date, get_weighted_choice
from src.utils.llm import generate_text_content
from datetime import datetime, timedelta
import random

TASK_TEMPLATES = {
    "Engineering": [
        "[Auth] - Fix login race condition",
        "[UI] - Refactor Navbar component",
        "[API] - Optimize /users endpoint",
        "[Db] - Add index to CreatedAt",
        "[Test] - Increase coverage for payment module"
    ],
    "Marketing": [
        "[Social] - Draft tweets for launch",
        "[Blog] - Review guest post",
        "[Email] - Set up drip campaign",
        "[Analyics] - Review Q2 traffic"
    ],
    "General": [
        "Update documentation",
        "Weekly sync notes",
        "Brainstorming session",
        "Review budget"
    ]
}

def generate_tasks(conn, generate_subtasks=True):
    print("Generating tasks...")
    cursor = conn.cursor()
    
    # helper for cache
    cursor.execute("SELECT project_id, team_id, created_at FROM projects")
    projects = cursor.fetchall()
    
    # Get all users for assignment
    cursor.execute("SELECT user_id, team_id FROM team_memberships")
    memberships = cursor.fetchall()
    team_members = {}
    for uid, tid in memberships:
        if tid not in team_members: team_members[tid] = []
        team_members[tid].append(uid)
        
    tasks_batch = []
    
    for proj in projects:
        p_id = proj['project_id']
        t_id = proj['team_id']
        p_created = datetime.fromisoformat(proj['created_at'])
        
        # Get sections
        cursor.execute("SELECT section_id FROM sections WHERE project_id = ?", (p_id,))
        sections = [r[0] for r in cursor.fetchall()]
        if not sections: continue
        
        potential_assignees = team_members.get(t_id, [])
        if not potential_assignees: continue
        
        # 10-30 tasks per project
        num_tasks = random.randint(10, 30)
        
        for _ in range(num_tasks):
            task_id = generate_uuid()
            section_id = random.choice(sections)
            creator_id = random.choice(potential_assignees)
            assignee_id = random.choice(potential_assignees + [None]) # Some unassigned
            
            # Name & Description
            # Heuristic: Check team dept? Just random for now or based on template
            base_name = random.choice(TASK_TEMPLATES.get("Engineering", TASK_TEMPLATES["General"])) # Simplification: random template
            # In a real run, we'd map project team dept to template
            
            name = base_name if random.random() > 0.1 else generate_text_content(f"Generate a realistic Asana task name for a {base_name} related task", "task_name")
            desc = generate_text_content("Write a 2 sentence description for this task", "task_description") if random.random() < 0.2 else ""
            
            created_at = p_created + timedelta(days=random.randint(0, 100))
            due_date = created_at + timedelta(days=random.randint(1, 30))
            
            priority = get_weighted_choice(['low', 'medium', 'high', None], [0.3, 0.4, 0.2, 0.1])
            completed = random.choice([True, False])
            completed_at = created_at + timedelta(days=random.randint(1, 14)) if completed else None
            
            if completed_at and completed_at > datetime.now():
                completed_at = datetime.now() # Cap at now
                
            tasks_batch.append((
                task_id, p_id, section_id, None, assignee_id, creator_id, name, desc, priority, due_date, None, completed, completed_at, created_at, created_at
            ))
            
            if len(tasks_batch) >= 1000:
                cursor.executemany("""
                    INSERT INTO tasks (task_id, project_id, section_id, parent_task_id, assignee_id, creator_id, name, description, priority, due_date, start_date, completed, completed_at, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tasks_batch)
                conn.commit()
                tasks_batch = []
    
    if tasks_batch:
        cursor.executemany("INSERT INTO tasks (task_id, project_id, section_id, parent_task_id, assignee_id, creator_id, name, description, priority, due_date, start_date, completed, completed_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tasks_batch)
        conn.commit()
        
    print("Tasks generation complete.")
