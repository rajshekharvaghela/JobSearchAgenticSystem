
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

def search_google_jobs(query, api_key):
    params = {
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "api_key": api_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    
    # Google Jobs returns a specific 'jobs_results' list
    return results.get("jobs_results", [])

if __name__ == "__main__":
    if not SERP_API_KEY:
        print("Error: SERP_API_KEY not found in .env file")
    else:
        query = "Python Backend Developer Remote"
        
        jobs = search_google_jobs(query, SERP_API_KEY)
    for job in jobs[:3]:
        print(f"Title: {job.get('title')}")
        print(f"Company: {job.get('company_name')}")
        print(f"Location: {job.get('location')}")
        print(f"Description Snippet: {job.get('description')[:100]}...")
        print("-" * 30)