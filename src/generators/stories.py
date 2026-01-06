import pandas as pd
import random
import os
from google import genai
from datetime import datetime, UTC
from dotenv import load_dotenv


load_dotenv()

# ---------------- CONFIG ----------------
MAX_HUMAN_COMMENTS = 3
SYSTEM_PROBABILITY = 0.7

STATUS_CONTEXT = {
    "Todo": "planning or clarifying requirements",
    "In Progress": "working on implementation and possibly facing blockers",
    "In Review": "requesting or giving review feedback",
    "Done": "confirming completion and outcomes"
}

SYSTEM_EVENTS = {
    "Todo": ["Task created", "Added to backlog"],
    "In Progress": ["Status changed to In Progress", "Assignee started work"],
    "In Review": ["Moved to In Review", "Review requested"],
    "Done": ["Task marked as Done", "Task closed"]
}

# ----------------------------------------

def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)
    return client

def generate_human_comment(client, task_title, status, role):
    prompt = f"""
You are a {role} in a B2B SaaS company using Asana.

Task: "{task_title}"
Current status: {status}

Write ONE short, realistic Asana-style comment reflecting {STATUS_CONTEXT[status]}.
No markdown. No emojis. 1-2 sentences.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("responded")
        return response.text.strip()
    except Exception as e:
        # print('Gemini Error',e)
        return None

def generate_stories():
    tasks = pd.read_csv("data/tasks.csv")
    users = pd.read_csv("data/users.csv")

    client = init_gemini()
    rows = []

    for _, task in tasks.iterrows():
        task_id = task["task_id"]
        status = task["status"]
        task_title = task["task_title"]

        # ---- SYSTEM EVENTS ----
        if random.random() < SYSTEM_PROBABILITY:
            for event in SYSTEM_EVENTS.get(status, []):
                rows.append({
                    "story_id": f"S-{random.randint(100000,999999)}",
                    "task_id": task_id,
                    "user_id": task["assigned_user_id"],
                    "text": event,
                    "type": "system",
                    "created_at": datetime.now(UTC).isoformat()
                })

        # ---- HUMAN COMMENTS ----
        n_comments = random.randint(0, MAX_HUMAN_COMMENTS)
        for _ in range(n_comments):
            user = users.sample(1).iloc[0]
            comment = generate_human_comment(
                client,
                task_title,
                status,
                user["role"]
            )

            if comment:
                rows.append({
                    "story_id": f"C-{random.randint(100000,999999)}",
                    "task_id": task_id,
                    "user_id": user["user_id"],
                    "text": comment,
                    "type": "comment",
                    "created_at": datetime.now(UTC).isoformat()
                })

    os.makedirs("data", exist_ok=True)
    pd.DataFrame(rows).to_csv("data/stories.csv", index=False)

    print(f"Created: data/stories.csv ({len(rows)} realistic comments & system events)")

if __name__ == "__main__":
    generate_stories()