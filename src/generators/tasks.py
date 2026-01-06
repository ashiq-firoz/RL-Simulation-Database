
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date, get_weighted_choice
from src.utils.llm import generate_text_content
from datetime import datetime, timedelta
import random
import pandas as pd

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
        
    # Load Task Patterns
    try:
        df_gh = pd.read_csv("src/scrapers/data/github_issues.csv")
        eng_patterns = df_gh["Title"].tolist()
        
        df_mkt = pd.read_csv("src/scrapers/data/marketing_tasks.csv")
        mkt_patterns = df_mkt.to_dict('records') # pattern, description
        
        df_gen = pd.read_csv("src/scrapers/data/general_tasks.csv")
        gen_patterns = df_gen.to_dict('records')
        
    except Exception as e:
        print(f"Warning: Could not load Task data ({e}). Using fallbacks.")
        eng_patterns = []
        mkt_patterns = []
        gen_patterns = []

    tasks_batch = []
    
    for proj in projects:
        p_id = proj['project_id']
        t_id = proj['team_id']
        p_created = datetime.fromisoformat(proj['created_at'])
        
        # Determine Dept context
        cursor.execute("SELECT name FROM teams WHERE team_id = ?", (t_id,))
        team_name = cursor.fetchone()[0]
        
        dept = "General"
        if "Engineer" in team_name or "Platform" in team_name or "Mobile" in team_name or "Data" in team_name:
            dept = "Engineering"
        elif "Marketing" in team_name or "Brand" in team_name:
            dept = "Marketing"

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
            assignee_id = random.choice(potential_assignees + [None])
            
            # Select Content based on Dept
            name = "New Task"
            desc = ""
            
            if dept == "Engineering" and eng_patterns:
                name = random.choice(eng_patterns)
                if random.random() < 0.2: desc = generate_text_content(f"Description for: {name}", "task_description")
            elif dept == "Marketing" and mkt_patterns:
                pat = random.choice(mkt_patterns)
                name = pat['pattern'].format(q=random.randint(1,4), month=random.choice(["Jan","Feb"]), product="App", page="Home", client="Acme", competitor="Rival", segment="SMB", topic="Growth", event="Summit", campaign="Q3 Launch")
                desc = pat['description']
            elif gen_patterns:
                pat = random.choice(gen_patterns)
                name = pat['pattern'].format(month=random.choice(["Jan","Feb"]), role="Manager", vendor="AWS", region="CA")
                desc = pat['description']
            else:
                 # Fallback
                 base_name = random.choice(TASK_TEMPLATES.get("General"))
                 name = base_name

            # LLM Override
            if random.random() < 0.05 and not desc: # Low prob
                 desc = generate_text_content(f"Write description for {name}", "task_description")
            
            created_at = p_created + timedelta(days=random.randint(0, 100))
            due_date = created_at + timedelta(days=random.randint(1, 30))

            # Start date: sometimes unset, otherwise between created_at and due_date
            if random.random() < 0.8:  # 80% tasks have start_date
                max_start_offset = max((due_date - created_at).days - 1, 0)
                start_date = created_at + timedelta(days=random.randint(0, max_start_offset))
            else:
                start_date = None

            
            priority = get_weighted_choice(['low', 'medium', 'high', None], [0.3, 0.4, 0.2, 0.1])

            if priority is None:
                priority = 'low'
            completed = random.choice([True, False])
            completed_at = created_at + timedelta(days=random.randint(1, 14)) if completed else None
            
            if completed_at and completed_at > datetime.now():
                completed_at = datetime.now() # Cap at now
                
            tasks_batch.append((
                task_id, p_id, section_id, None, assignee_id, creator_id, name, desc, priority, due_date, start_date, completed, completed_at, created_at, created_at
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
