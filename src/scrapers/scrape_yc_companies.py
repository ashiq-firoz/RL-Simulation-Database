import requests
import csv
import os

def scrape_yc_companies():
    """
    Scrapes YC companies using YC's public JSON API
    """
    url = "https://api.ycombinator.com/v0.1/companies"

    output_file = "src/scrapers/data/yc_companies.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        print(f"Fetching YC data from {url}...")
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        data = response.json()

        companies = []
        for c in data:
            name = c.get("name")
            website = c.get("website")

            if name and website:
                website = website.replace("https://", "").replace("http://", "").rstrip("/")
                companies.append((name, website))

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["company_name", "domain"])
            writer.writerows(companies[:500])

        print(f"Successfully saved {min(500, len(companies))} companies to {output_file}")

    except Exception as e:
        print(f"Scraping failed: {e}")
        _write_fallback(output_file)


def _write_fallback(output_file):
    companies = [
        ("Stripe", "stripe.com"),
        ("Airbnb", "airbnb.com"),
        ("DoorDash", "doordash.com"),
        ("Coinbase", "coinbase.com"),
        ("Dropbox", "dropbox.com"),
        ("GitLab", "gitlab.com"),
        ("Reddit", "reddit.com"),
        ("Twitch", "twitch.tv"),
        ("PagerDuty", "pagerduty.com"),
        ("Brex", "brex.com"),
        ("Faire", "faire.com"),
        ("Deel", "deel.com"),
        ("Rippling", "rippling.com"),
        ("Gusto", "gusto.com"),
        ("Scale AI", "scale.com"),
    ]

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["company_name", "domain"])
        writer.writerows(companies)

    print(f"Created fallback data with {len(companies)} companies.")


if __name__ == "__main__":
    scrape_yc_companies()
