import os
from dotenv import load_dotenv
from src.database import collection
from src.tools.web_search import search_and_read
from src.tools.serp_job_search import search_google_jobs
from src.evaluator import evaluate_jobs

load_dotenv()
SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

def run_job_search_agent(query, use_premium=False):
    print(f"🚀 Starting Agentic Search for: '{query}'")
    
    # Phase 1: Discovery
    all_jobs = []
    
    # Try the free tool first (DDGS)
    print("📡 Querying DuckDuckGo (Primary/Free)...")
    ddgs_results = search_and_read(f"site:lever.co OR site:greenhouse.io {query}")
    all_jobs.extend(ddgs_results)
    
    # Optional: Use SerpApi if explicitly requested or if DDGS found nothing
    if use_premium and SERP_API_KEY:
        print("📡 Querying SerpApi (Premium/High-Fidelity)...")
        serp_results = search_google_jobs(query, SERP_API_KEY)
        all_jobs.extend(serp_results)

    # Phase 2: Evaluation & Ranking
    # We set a threshold of 0.45 based on our 'Chef vs. Engineer' test
    matches = evaluate_jobs(all_jobs, threshold=0.45)

    # Phase 3: Final Report
    print("\n" + "="*50)
    print(f"✅ AGENT REPORT: Found {len(matches)} relevant jobs.")
    print("="*50)

    for i, job in enumerate(matches, 1):
        title = job.get('title')
        company = job.get('company_name') or "Unknown Company"
        score = job.get('match_score')
        link = job.get('link') or job.get('registration_url')
        
        print(f"{i}. [{score}] {title} @ {company}")
        print(f"   🔗 Link: {link}\n")

if __name__ == "__main__":
    # Example search query combining your preferences
    user_query = "Python Backend Developer Remote"
    
    # Set use_premium=True if you want to use your SerpApi credits
    run_job_search_agent(user_query, use_premium=False)