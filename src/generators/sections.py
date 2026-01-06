import pandas as pd
import os

def generate_sections():
    projects = pd.read_csv("data/projects.csv")

    default_sections = ["Backlog", "Todo", "In Progress", "In Review", "Done"]
    rows = []

    for _, p in projects.iterrows():
        for idx, name in enumerate(default_sections):
            rows.append({
                "section_id": f"S-{p['p_id']}-{idx}",
                "project_id": p["p_id"],
                "name": name,
                "order_index": idx
            })

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(rows).to_csv("data/sections.csv", index=False)
    print("Created: data/sections.csv")

if __name__ == "__main__":
    generate_sections()
