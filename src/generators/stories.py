
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
from src.utils.llm import generate_text_content
from datetime import datetime, timedelta
import random
import pandas as pd

COMMENT_TEMPLATES = [
    "Can you clarify the requirements?",
    "I'll pick this up tomorrow.",
    "Blocked by API unavailability.",
    "Ready for review.",
    "LGTM!",
    "Please update the docs."
]

def generate_stories(conn):
    print("Generating stories (comments)...")
    cursor = conn.cursor()
    
    # Get tasks to attach stories to
    cursor.execute("SELECT task_id, created_at, completed_at, assignee_id, creator_id, completed FROM tasks WHERE completed = 1 LIMIT 5000") # Limit for performance
    tasks = cursor.fetchall()
    
    # Get a pool of users (simplification: random users for now, ideally team members)
    cursor.execute("SELECT user_id FROM users LIMIT 100")
    users = [r[0] for r in cursor.fetchall()]
    
    # Load Comments Data
    try:
        df_comm = pd.read_csv("src/scrapers/data/comments.csv")
        eng_comments = df_comm[(df_comm['category'] == 'Engineering') & (df_comm['type'] == 'comment')]['content'].tolist()
        mkt_comments = df_comm[(df_comm['category'] == 'Marketing') & (df_comm['type'] == 'comment')]['content'].tolist()
        gen_comments = df_comm[(df_comm['category'] == 'General') & (df_comm['type'] == 'comment')]['content'].tolist()
        
        system_events = df_comm[df_comm['type'] == 'system']['content'].tolist()
    except Exception as e:
        print(f"Warning: Could not load comments ({e}). Using falbacks.")
        eng_comments = COMMENT_TEMPLATES
        mkt_comments = COMMENT_TEMPLATES
        gen_comments = COMMENT_TEMPLATES
        system_events = ["Task Assigned", "Task Completed"]

    stories_batch = []
    
    for task in tasks:
        t_id = task['task_id']
        t_created = datetime.fromisoformat(task['created_at'])
        t_completed = datetime.fromisoformat(task['completed_at']) if task['completed_at'] else datetime.now()
        
        # Determine likely category based on random chance or if we had task category (We don't store it, so heuristic)
        # 40% Eng, 30% Mkt, 30% Gen
        r = random.random()
        if r < 0.4: comments_pool = eng_comments
        elif r < 0.7: comments_pool = mkt_comments
        else: comments_pool = gen_comments
        
        # 0-5 stories per task
        num_stories = random.choices([0, 1, 2, 3, 4, 5], weights=[0.2, 0.2, 0.2, 0.2, 0.1, 0.1])[0]
        
        # Always add a system event for completed tasks?
        events = []
        if task['completed']:
             uid = task['assignee_id'] if task['assignee_id'] else task['creator_id']
             events.append(("Task Completed", t_completed, uid, 'system'))
        
        # Add random comments/events
        for _ in range(num_stories):
            is_system = random.random() < 0.3
            if is_system:
                txt = random.choice(system_events)
                # If assigned, say "Task Assigned to X"
                if txt == "Task Assigned" and task['assignee_id']:
                    txt = "Task Assigned" # Simplification for now
                uid = task['assignee_id'] if task['assignee_id'] else task['creator_id'] # System events usually by someone
            else:
                txt = random.choice(comments_pool)
                uid = random.choice(users) # Random commenter
            
            # Timestamp
            delta = (t_completed - t_created).total_seconds()
            if delta > 0:
                s_created = t_created + timedelta(seconds=random.randint(0, int(delta)))
            else:
                s_created = t_created
            
            events.append((txt, s_created, uid, 'system' if is_system else 'comment'))
            
        for txt, time, uid, stype in events:
            s_id = generate_uuid()
            stories_batch.append((s_id, t_id, uid, txt, stype, time))
            
            if len(stories_batch) >= 1000:
                cursor.executemany("INSERT INTO stories (story_id, task_id, user_id, text, type, created_at) VALUES (?, ?, ?, ?, ?, ?)", stories_batch)
                conn.commit()
                stories_batch = []

    if stories_batch:
        cursor.executemany("INSERT INTO stories (story_id, task_id, user_id, text, type, created_at) VALUES (?, ?, ?, ?, ?, ?)", stories_batch)
        conn.commit()
        
    print("Stories generation complete.")