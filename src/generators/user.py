import pandas as pd
import random
import os

def generate_users(n=50):
    team_role_map = {
        "Infrastructure": [
            "Site Reliability Engineer", "Cloud Architect", "DevOps Engineer", 
            "Security Analyst", "Network Engineer", "Technical Project Manager"
        ],
        "Product-Web": [
            "Full Stack Developer", "Frontend Engineer", "Backend Engineer", 
            "Product Manager", "QA Automation Engineer", "UX Researcher"
        ],
        "Growth": [
            "Growth Marketer", "Performance Marketing Manager", "SEO Specialist", 
            "Data Analyst", "Lifecycle Email Marketer", "Conversion Rate Optimizer"
        ],
        "Data-Science": [
            "Data Scientist", "Machine Learning Engineer", "Data Engineer", 
            "BI Developer", "AI Research Scientist", "Analytics Manager"
        ],
        "Brand-Design": [
            "Product Designer", "Visual Designer", "Creative Director", 
            "Brand Strategist", "Copywriter", "Motion Graphics Artist"
        ]
    }

    first_names = [
        "Liam", "Yuki", "Aarav", "Elena", "Mateo", "Priya", "Chen", "Sasha", 
        "Amara", "Finn", "Zoe", "Hiroshi", "Fatima", "Lars", "Ji-won", "Noa"
    ]
    last_names = [
        "Smith", "Tanaka", "Iyer", "Petrov", "Silva", "Gupta", "Wang", "O'Connor", 
        "Abbe", "Johansson", "Park", "Cohen", "Müller", "Rodriguez", "Sato", "Kim"
    ]

    users = []
    teams = list(team_role_map.keys())

    for i in range(1, n + 1):
        # Pick a team first
        team = random.choice(teams)
        # Pick a role valid for that team
        role = random.choice(team_role_map[team])
        
        f = random.choice(first_names)
        l = random.choice(last_names)
        
        users.append({
            "user_id": f"U-{100 + i}",
            "name": f"{f} {l}",
            "email": f"{f.lower()}.{l.lower()}@startup.io",
            "team": team,
            "role": role,
            "seniority": random.choice(["Junior", "Mid-Level", "Senior", "Staff", "Lead"])
        })

    os.makedirs('data', exist_ok=True)
    pd.DataFrame(users).to_csv("data/users.csv", index=False)
    print(f"Generated {n} realistic users in data/users.csv")

if __name__ == "__main__":
    generate_users(50)