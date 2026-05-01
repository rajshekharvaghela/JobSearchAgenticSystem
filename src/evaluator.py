from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from src.database import collection, model

def evaluate_jobs(job_list, threshold=0.45):
    """
    Takes a list of jobs from DDGS or SerpApi and ranks them 
    against the stored resume in MongoDB.
    """
    # 1. Fetch your 'Anchor' Resume Vector
    user = collection.find_one({"name": "User"})
    if not user:
        print("No user profile found in DB. Run database.py first.")
        return []
    
    resume_vector = [user["resume_vector"]]
    matches = []

    print(f"\n--- Evaluating {len(job_list)} Jobs ---")

    for job in job_list:
        # Use description or snippet for the vector comparison
        text_to_evaluate = job.get('description') or job.get('full_content') or job.get('snippet')
        
        if not text_to_evaluate:
            continue

        # 2. Vectorize the job listing
        job_vector = [model.encode(text_to_evaluate).tolist()]
        
        # 3. Calculate Score
        score = cosine_similarity(resume_vector, job_vector)[0][0]
        
        if score >= threshold:
            job['match_score'] = round(float(score), 4)
            matches.append(job)

    # Sort by highest match score
    return sorted(matches, key=lambda x: x['match_score'], reverse=True)

if __name__ == "__main__":
    # This is where you would call your search_google_jobs or search_and_read
    # For now, you can import your tools and pass the results here!
    print("Evaluator ready to process job lists.")