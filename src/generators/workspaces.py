import pandas as pd
import os
from uuid import uuid4

def generate_workspaces():
    workspaces = [{
        "workspace_id": str(uuid4()),
        "name": "Acme SaaS Inc.",
        "domain": "acme-saas.com"
    }]

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(workspaces).to_csv("data/workspaces.csv", index=False)
    print("Created: data/workspaces.csv")

if __name__ == "__main__":
    generate_workspaces()
