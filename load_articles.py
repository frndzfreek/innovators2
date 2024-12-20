import json
import os

# Load the articles from the JSON file
def load_articles():
    data_path = 'data/articles/incident_solutions.json'
    if os.path.exists(data_path):
        with open(data_path, 'r') as file:
            articles = json.load(file)
            print(f"Loaded {len(articles)} articles.")  # Check how many articles were loaded
            return articles
    else:
        print("Error: articles file not found.")
        return []

# Example of using the function
articles = load_articles()

# Print the first article and its incidents
if articles:
    for idx, article in enumerate(articles):
        print(f"Article {idx + 1} Category: {article['category']}")
        for incident in article['incidents']:
            print(f"- Incident Title: {incident['incident_title']}, Severity: {incident['severity']}, Solution: {incident['solution']}")
else:
    print("No articles found.")
