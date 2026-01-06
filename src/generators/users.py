
from faker import Faker
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
from datetime import datetime, timedelta
import random

fake = Faker()

JOB_TITLES = {
    "Engineering": [
        ("Software Engineer", 0.4), ("Senior Software Engineer", 0.3), 
        ("Staff Engineer", 0.1), ("Engineering Manager", 0.1),
        ("DevOps Engineer", 0.05), ("QA Engineer", 0.05)
    ],
    "Product": [
        ("Product Manager", 0.4), ("Senior PM", 0.3),
        ("Group PM", 0.1), ("Designer", 0.2)
    ],
    "Marketing": [("Marketing Specialist", 0.5), ("Content Writer", 0.3), ("SEO Manager", 0.2)],
    "Sales": [("Sales Representative", 0.6), ("Account Executive", 0.3), ("Sales Manager", 0.1)],
    "Operations": [("HR Specialist", 0.4), ("Recruiter", 0.3), ("Office Manager", 0.3)]
}

def generate_users(conn, workspace_id, count=5000):
    print(f"Generating {count} users...")
    cursor = conn.cursor()
    
    users_data = []
    base_date = datetime.now() - timedelta(days=365*5)
    
    # Pre-generate emails to ensure uniqueness
    emails = set()
    while len(emails) < count:
        emails.add(fake.unique.email())
    emails = list(emails)

    for i in range(count):
        user_id = generate_uuid()
        
        # Pick a department and role
        dept = random.choice(list(JOB_TITLES.keys()))
        titles, weights = zip(*JOB_TITLES[dept])
        job_title = random.choices(titles, weights=weights, k=1)[0]
        
        full_name = fake.name()
        email = emails[i]
        avatar_url = fake.image_url()
        
        # Growth curve: more users joined recently
        days_since_start = int((datetime.now() - base_date).days * (random.random() ** 0.5)) 
        joined_at = base_date + timedelta(days=days_since_start)

        users_data.append((
            user_id, workspace_id, email, full_name, job_title, avatar_url, joined_at
        ))
        
        if len(users_data) >= 1000:
            cursor.executemany("""
                INSERT INTO users (user_id, workspace_id, email, full_name, job_title, avatar_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, users_data)
            conn.commit()
            users_data = []
            print(f"Inserted {i+1} users...")

    if users_data:
        cursor.executemany("""
            INSERT INTO users (user_id, workspace_id, email, full_name, job_title, avatar_url, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, users_data)
        conn.commit()

    print("User generation complete.")
