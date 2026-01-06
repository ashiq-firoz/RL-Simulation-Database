
import csv
import os

def generate_marketing_csv():
    """
    Generates a CSV of realistic marketing task patterns.
    Pattern: Template string with {variables} to be filled at runtime.
    """
    data = [
        ("Draft Q{q} Social Media Calendar", "Create content schedule for upcoming quarter"),
        ("Design assets for {campaign}", "Visuals for social and email"),
        ("Analyze {month} Traffic Report", "Review Google Analytics and search console"),
        ("Launch {product} GTM Campaign", "Full funnel marketing blast"),
        ("Optimize {page} Landing Page", "A/B test headlines and CTAs"),
        ("Write Case Study: {client}", "Interview client and draft success story"),
        ("Review Competitor Ads: {competitor}", "Analyze ad spend and creative strategy"),
        ("Setup Drip Campaign: {segment}", "Onboarding email sequence for new signups"),
        ("Coordinate Webinar: {topic}", "Speaker logistics and promotion"),
        ("Update SEO Keywords", "Review rankings and optimize content"),
        ("Plan {event} Booth", "Design booth layout/swag"),
        ("Audit Brand Voice", "Review website copy for consistency"),
        ("Weekly Marketing Sync", "Update on KPIs and blockers"),
        ("Review Ad Spend", "Optimize CAC and ROAS")
    ]
    
    output_file = "src/scrapers/data/marketing_tasks.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['pattern', 'description'])
        writer.writerows(data)
        
    print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_marketing_csv()
