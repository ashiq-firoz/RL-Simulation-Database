import pandas as pd
import os
from uuid import uuid4

def generate_custom_fields():
    workspace_id = pd.read_csv("data/workspaces.csv").iloc[0]["workspace_id"]

    fields = [
        ("Story Points", "number"),
        ("Severity", "enum"),
        ("Customer Impact", "boolean"),
        ("Target Release", "date")
    ]

    rows = [{
        "field_id": str(uuid4()),
        "workspace_id": workspace_id,
        "name": name,
        "type": ftype
    } for name, ftype in fields]

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(rows).to_csv("data/custom_field_definitions.csv", index=False)
    print("Created: data/custom_field_definitions.csv")

if __name__ == "__main__":
    generate_custom_fields()
