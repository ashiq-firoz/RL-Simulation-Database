import pandas as pd
import os
from uuid import uuid4

def generate_teams():
    teams = [
        "Infrastructure", "Product-Web", "Growth",
        "Data-Science", "Brand-Design", "Security", "Operations"
    ]

    workspace_id = pd.read_csv("data/workspaces.csv").iloc[0]["workspace_id"]

    rows = [{
        "team_id": str(uuid4()),
        "workspace_id": workspace_id,
        "name": t
    } for t in teams]

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(rows).to_csv("data/teams.csv", index=False)
    print("Created: data/teams.csv")

if __name__ == "__main__":
    generate_teams()
