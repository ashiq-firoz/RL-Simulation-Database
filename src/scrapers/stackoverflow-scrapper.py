import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_stackoverflow_titles(limit=50):
    url = "https://stackoverflow.com/questions?tab=newest"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    titles_collected = []
    page = 1
    
    print("Scraping StackOverflow...")
    
    while len(titles_collected) < limit:
        response = requests.get(f"{url}&page={page}", headers=headers)
        
        if response.status_code != 200:
            print("Blocked or Error. Try again later.")
            break
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        questions = soup.select(".s-post-summary--content-title a")
        
        for q in questions:
            if len(titles_collected) < limit:
                titles_collected.append([q.get_text(strip=True)])
            else:
                break
        
        page += 1
        time.sleep(1)
        
    return titles_collected

if __name__ == "__main__":
    data = scrape_stackoverflow_titles(100)
    
    if data:
        with open("data/stackoverflow_titles.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Title"])
            writer.writerows(data)
        print(f"Success! {len(data)} titles saved to 'stackoverflow_titles.csv'.")