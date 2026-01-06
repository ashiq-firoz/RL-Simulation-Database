import pandas as pd
import random
import os

def generate_tasks(tasks_per_project=15):
    try:
        # Adjusted paths to match your scraper and data directory structure
        github = pd.read_csv("../scrapers/data/github_issues.csv")["Title"].tolist()
        stack = pd.read_csv("../scrapers/data/stackoverflow_titles.csv")["Title"].tolist()
        patterns = pd.read_csv("../scrapers/data/strategy_patterns.csv")
        
        users = pd.read_csv("data/users.csv")
        projects = pd.read_csv("data/projects.csv")
    except Exception as e:
        print(f"Error loading files: {e}. Ensure source CSVs are in the root.")
        return

    # Categorize patterns
    eng_patterns = patterns[patterns['Category'] == 'Engineering']['Task Pattern'].tolist()
    mkt_patterns = patterns[patterns['Category'] == 'Marketing']['Task Pattern'].tolist()
    
    # Combined pool for technical projects
    engineering_pool = github + stack + eng_patterns

    all_tasks = []
    
    for _, project in projects.iterrows():
        # Filter users by team
        team_users = users[users['team'] == project['team']]
        
        if team_users.empty:
            continue

        for _ in range(tasks_per_project):
            # 1. Determine Priority
            priority = random.choice(["Low", "Medium", "High", "Critical"])
            
            # 2. Seniority-Based Assignment Logic
            # Critical tasks favor Senior/Staff/Lead users
            if priority in ["Critical", "High"]:
                seniors = team_users[team_users['seniority'].isin(["Senior", "Staff", "Lead"])]
                pool = seniors if not seniors.empty else team_users
            else:
                juniors = team_users[team_users['seniority'].isin(["Junior", "Mid-Level"])]
                pool = juniors if not juniors.empty else team_users
            
            assigned_user = pool.sample(1).iloc[0]

            # 3. Context-Aware Title Selection
            if project['type'] in ["Engineering", "Security"]:
                title = random.choice(engineering_pool)
            else:
                title = random.choice(mkt_patterns)

            # 4. Realistic Status Distribution
            # Most tasks are 'Todo' or 'In Progress', fewer are 'Done' in seed data
            status = random.choices(
                ["Todo", "In Progress", "In Review", "Done"], 
                weights=[40, 30, 20, 10], k=1
            )[0]

            all_tasks.append({
                "task_id": f"T-{random.randint(10000, 99999)}",
                "project_id": project['p_id'],
                "project_name": project['name'], # Added for easier debugging
                "assigned_user_id": assigned_user['user_id'],
                "assigned_user_name": assigned_user['name'],
                "seniority": assigned_user['seniority'],
                "task_title": title,
                "priority": priority,
                "status": status,
                "created_at": f"2026-0{random.randint(1,3)}-{random.randint(10,28)}"
            })

    os.makedirs('data', exist_ok=True)
    df_tasks = pd.DataFrame(all_tasks)
    df_tasks.to_csv("data/tasks.csv", index=False)
    
    print(f"Created: data/tasks.csv ({len(df_tasks)} Tasks)")
    print("\n--- Seniority Assignment Check ---")
    print(df_tasks.groupby(['priority', 'seniority']).size().unstack(fill_value=0))

if __name__ == "__main__":
    generate_tasks()