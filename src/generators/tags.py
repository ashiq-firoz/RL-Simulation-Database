import pandas as pd
import os

def generate_tags():
    tags = [
        ("frontend", "blue"),
        ("backend", "green"),
        ("security", "red"),
        ("growth", "purple"),
        ("infra", "orange")
    ]

    workspace_id = pd.read_csv("data/workspaces.csv").iloc[0]["workspace_id"]

    rows = [{
        "tag_id": f"T-{i}",
        "workspace_id": workspace_id,
        "name": name,
        "color": color
    } for i, (name, color) in enumerate(tags)]

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(rows).to_csv("data/tags.csv", index=False)
    print("Created: data/tags.csv")

if __name__ == "__main__":
    generate_tags()
