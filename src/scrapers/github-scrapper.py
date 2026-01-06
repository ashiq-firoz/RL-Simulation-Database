import requests
import pandas as pd

def scrape_github_issues(owner, repo, limit=50):
    """
    Fetches the latest issue titles from a public GitHub repository.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    params = {
        "state": "all",      
        "per_page": limit,    
        "page": 1
    }
    
    print(f"Fetching data from GitHub ({owner}/{repo})...")
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        issues = response.json()
        data = []
        
        for issue in issues:
            data.append({
                "Source": "GitHub",
                "Title": issue['title'],
                "URL": issue['html_url']
            })
            
        return data
    else:
        print(f"Error: {response.status_code}")
        return []

if __name__ == "__main__":
    # Scraping pandas-dev repo
    scraped_data = scrape_github_issues("pandas-dev", "pandas", limit=100)
    
    if scraped_data:
        df = pd.DataFrame(scraped_data)
        df.to_csv("data/github_issues.csv", index=False)
        print(f"Success! {len(df)} titles saved to 'github_issues.csv'.")
        print("First 3 titles:", df['Title'].head(3).tolist())
    else:
        print("No data found.")