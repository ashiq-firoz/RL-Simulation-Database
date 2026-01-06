
import csv
import os

def generate_comments_csv():
    """
    Generates a CSV of comment templates and system events.
    Columns: category, type, content
    """
    
    # (Category, Type, Content)
    data = [
        # Engineering Comments
        ("Engineering", "comment", "Can we check the logs for this?"),
        ("Engineering", "comment", "I think this is related to the recent migration."),
        ("Engineering", "comment", "LGTM. Merging now."),
        ("Engineering", "comment", "Added unit tests."),
        ("Engineering", "comment", "Blocking issue on the API side."),
        
        # Marketing Comments
        ("Marketing", "comment", "Can you use the new color palette?"),
        ("Marketing", "comment", "Copy looks good, but title needs punch."),
        ("Marketing", "comment", "Scheduled for next Tuesday."),
        ("Marketing", "comment", "Waiting on design assets."),
        
        # General Comments
        ("General", "comment", "APPROVED."),
        ("General", "comment", "Please attach the invoice."),
        ("General", "comment", "Let's discuss in the sync."),
        ("General", "comment", "Updated the spreadsheet."),
        
        # System Events
        ("All", "system", "Task Created"),
        ("All", "system", "Due Date Changed"),
        ("All", "system", "Task Assigned"),
        ("All", "system", "Task Completed"),
        ("All", "system", "Task Closed")
    ]
    
    output_file = "src/scrapers/data/comments.csv"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['category', 'type', 'content'])
        writer.writerows(data)
        
    print(f"Generated {output_file}")

if __name__ == "__main__":
    generate_comments_csv()
