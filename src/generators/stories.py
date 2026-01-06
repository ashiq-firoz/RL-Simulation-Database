
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
from src.utils.llm import generate_text_content
from datetime import datetime, timedelta
import random

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
    cursor.execute("SELECT task_id, created_at, completed_at, assignee_id FROM tasks WHERE completed = 1 LIMIT 5000") # Limit for performance
    tasks = cursor.fetchall()
    
    # Get a pool of users (simplification: random users for now, ideally team members)
    cursor.execute("SELECT user_id FROM users LIMIT 100")
    users = [r[0] for r in cursor.fetchall()]
    
    stories_batch = []
    
    for task in tasks:
        t_id = task['task_id']
        t_created = datetime.fromisoformat(task['created_at'])
        t_completed = datetime.fromisoformat(task['completed_at']) if task['completed_at'] else datetime.now()
        
        # 0-3 comments
        num_comments = random.choices([0, 1, 2, 3], weights=[0.4, 0.3, 0.2, 0.1])[0]
        
        for _ in range(num_comments):
            s_id = generate_uuid()
            user_id = task['assignee_id'] if task['assignee_id'] and random.random() > 0.5 else random.choice(users)
            
            text = random.choice(COMMENT_TEMPLATES)
            if random.random() < 0.1:
                text = generate_text_content("Write a short professional comment on a task", "comment")
                
            # Random time between creation and completion
            delta = (t_completed - t_created).total_seconds()
            if delta > 0:
                c_created = t_created + timedelta(seconds=random.randint(0, int(delta)))
            else:
                c_created = t_created
                
            stories_batch.append((s_id, t_id, user_id, text, 'comment', c_created))
            
            if len(stories_batch) >= 1000:
                cursor.executemany("INSERT INTO stories (story_id, task_id, user_id, text, type, created_at) VALUES (?, ?, ?, ?, ?, ?)", stories_batch)
                conn.commit()
                stories_batch = []

    if stories_batch:
        cursor.executemany("INSERT INTO stories (story_id, task_id, user_id, text, type, created_at) VALUES (?, ?, ?, ?, ?, ?)", stories_batch)
        conn.commit()
        
    print("Stories generation complete.")