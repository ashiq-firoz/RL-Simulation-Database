
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.scrapers.scrape_yc_companies import scrape_yc_companies
from src.scrapers.fetch_census_data import fetch_census_names
from src.scrapers.generate_marketing_tasks import generate_marketing_csv
from src.scrapers.generate_comment_templates import generate_comments_csv


def run_all_scrapers():
    print("=== Running Data Scrapers/Generators ===")
    
    print("\n1. Y Combinator Companies")
    scrape_yc_companies()
    
    print("\n2. Census Names")
    fetch_census_names()
    
    print("\n3. Marketing Task Patterns")
    generate_marketing_csv()
    
    print("\n4. Comment Templates")
    generate_comments_csv()
    
    print("\n=== Data Generation Complete ===")
    print("Files saved to src/scrapers/data/")

if __name__ == "__main__":
    run_all_scrapers()
