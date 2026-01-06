
from faker import Faker
from src.utils.db import get_connection
from src.utils.helpers import generate_uuid, random_date
from datetime import datetime, timedelta
import random
import pandas as pd

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

def generate_users(conn, workspace_id, domain="startup.io", count=5000):
    print(f"Generating {count} users...")
    cursor = conn.cursor()
    
    users_data = []
    base_date = datetime.now() - timedelta(days=365*5)
    emails = set()
    
    # Load Census Names
    try:
        df_names = pd.read_csv("src/scrapers/data/census_names.csv")
        first_names = df_names['first_name'].tolist()
        last_names = df_names['last_name'].tolist()
        probs = df_names['probability'].tolist()
        # Normalise probs
        total_prob = sum(probs)
        probs = [p/total_prob for p in probs]
    except Exception as e:
        print(f"Warning: Could not load Census data ({e}). Using Faker.")
        first_names, last_names, probs = [], [], []

    for i in range(count):
        user_id = generate_uuid()
        
        # Pick a department and role
        dept = random.choice(list(JOB_TITLES.keys()))
        titles, weights = zip(*JOB_TITLES[dept])
        job_title = random.choices(titles, weights=weights, k=1)[0]
        
        if first_names:
            # Weighted random name
            fname = random.choices(first_names, weights=probs, k=1)[0]
            lname = random.choices(last_names, weights=probs, k=1)[0]
            full_name = f"{fname} {lname}"
            
            # Ensure unique email
            base_email = f"{fname.lower()}.{lname.lower()}"
            email = f"{base_email}@{domain}"
            counter = 1
            while email in emails:
                email = f"{base_email}{counter}@{domain}"
                counter += 1
            emails.add(email)
        else:
            full_name = fake.name()
            email = fake.unique.email()
            emails.add(email)
            
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
