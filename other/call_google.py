import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

def google_search(search_term, api_key, cse_id, **kwargs):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': search_term,
        'key': api_key,
        'cx': cse_id,
    }
    
    # Add any other requested arguments
    for key, value in kwargs.items():
        params[key] = value

    response = requests.get(url, params=params)
    
    return response.json()

# Test the function
if __name__ == '__main__':
    api_key = os.getenv("GOOGLE_API_KEY")
    cse_id = os.getenv("GOOGLE_CSE_ID")
    search_term = "OpenAI"
    print(api_key)
    print(cse_id)

    results = google_search(
        search_term, api_key, cse_id, num=10
    )

    # Pretty-print the JSON
    print(json.dumps(results, indent=2))