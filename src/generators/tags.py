
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
import random

COLORS = ["red", "green", "blue", "yellow", "orange", "purple", "grey"]
TAG_NAMES = ["Bug", "Feature", "Q1", "Priority", "Design", "Backend", "Frontend", "Blocked", "Release"]

def generate_tags(conn, workspace_id):
    print("Generating tags...")
    cursor = conn.cursor()
    
    tags = []
    
    for name in TAG_NAMES:
        t_id = generate_uuid()
        color = random.choice(COLORS)
        tags.append((t_id, workspace_id, name, color))
        
    cursor.executemany("INSERT INTO tags (tag_id, workspace_id, name, color) VALUES (?, ?, ?, ?)", tags)
    conn.commit()
    
    # Assign tags to tasks
    print("Assigning tags to tasks...")
    cursor.execute("SELECT task_id FROM tasks LIMIT 5000") # Sample
    tasks = cursor.fetchall()
    
    task_tags = []
    
    for task in tasks:
        if random.random() < 0.3: # 30% of tasks have tags
            num_tags = random.randint(1, 3)
            selected_tags = random.sample(tags, k=min(num_tags, len(tags)))
            for t_data in selected_tags:
                task_tags.append((task['task_id'], t_data[0]))
                
    cursor.executemany("INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)", task_tags)
    conn.commit()
    print("Tags generation complete.")
