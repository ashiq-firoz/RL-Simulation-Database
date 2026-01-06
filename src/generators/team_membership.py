import pandas as pd
import random
import os

def generate_team_memberships():
    users = pd.read_csv("data/users.csv")
    teams = pd.read_csv("data/teams.csv")

    memberships = []

    for _, user in users.iterrows():
        assigned_teams = random.sample(
            list(teams["team_id"]),
            k=random.randint(1, 3)
        )

        for t in assigned_teams:
            memberships.append({
                "user_id": user["user_id"],
                "team_id": t,
                "role": random.choice(["member", "admin"])
            })

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(memberships).to_csv("data/team_memberships.csv", index=False)
    print("Created: data/team_memberships.csv")

if __name__ == "__main__":
    generate_team_memberships()
