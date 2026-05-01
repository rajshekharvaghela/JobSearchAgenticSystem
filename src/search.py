from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from database import collection, model # Import from your setup script

def mock_search():
    # 1. Get your stored resume vector from MongoDB
    user = collection.find_one({"name": "User"})
    resume_vector = [user["resume_vector"]]

    # 2. Mock Job Descriptions
    jobs = [
        {
            "title": "Backend Engineer",
            "desc": "Looking for a Python developer who knows MongoDB and JavaScript."
        },
        {
            "title": "Chef",
            "desc": "Required experience in Italian cuisine and making pasta from scratch."
        }
    ]

    print("--- Testing Similarity ---")
    for job in jobs:
        # Convert job description to a vector
        job_vector = [model.encode(job["desc"]).tolist()]
        
        # Calculate how close they are (Result is between 0 and 1)
        score = cosine_similarity(resume_vector, job_vector)[0][0]
        
        print(f"Job: {job['title']} | Match Score: {score:.4f}")

if __name__ == "__main__":
    mock_search()