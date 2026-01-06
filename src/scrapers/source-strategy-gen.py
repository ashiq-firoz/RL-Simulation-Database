import random
import pandas as pd

def generate_strategy_lists(n=20):
    # --- Engineering Patterns Data ---
    eng_verbs = ["Refactor", "Fix", "Optimize", "Implement", "Deprecate", "Migrate", "Debug", "Dockerize", "Scale"]
    eng_nouns = ["API authentication", "database schema", "Redis caching", "React components", "payment gateway", "CI/CD pipeline", "memory leak", "OAuth flow"]
    eng_context = ["for legacy support", "to reduce latency", "in the microservices", "before next release", "causing 500 errors", "for mobile users"]

    # --- Marketing Patterns Data ---
    mkt_verbs = ["A/B Test", "Draft", "Launch", "Analyze", "Optimize", "Design", "Schedule", "Audit", "Refresh"]
    mkt_nouns = ["landing page copy", "Q3 newsletter", "Facebook ad creatives", "SEO keywords", "competitor backlink profile", "drip campaign", "onboarding email sequence"]
    mkt_context = ["to boost conversion", "for upcoming webinar", "targeting SaaS founders", "to improve CTR", "using new brand voice", "for holiday promotion"]

    strategies = []

    # Generate Engineering Tasks
    for _ in range(n):
        task = f"{random.choice(eng_verbs)} {random.choice(eng_nouns)} {random.choice(eng_context)}"
        strategies.append({"Category": "Engineering", "Task Pattern": task})

    # Generate Marketing Tasks
    for _ in range(n):
        task = f"{random.choice(mkt_verbs)} {random.choice(mkt_nouns)} {random.choice(mkt_context)}"
        strategies.append({"Category": "Marketing", "Task Pattern": task})

    return strategies

if __name__ == "__main__":
    data = generate_strategy_lists(50) 
    
    df = pd.DataFrame(data)
    df.to_csv("data/strategy_patterns.csv", index=False)
    
    print("Success! Generated strategy patterns.")
    # print("\n--- Sample Engineering Tasks ---")
    # print(df[df['Category'] == 'Engineering']['Task Pattern'].head(5).to_string(index=False))
    # print("\n--- Sample Marketing Tasks ---")
    # print(df[df['Category'] == 'Marketing']['Task Pattern'].head(5).to_string(index=False))