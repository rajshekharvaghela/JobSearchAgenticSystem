from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

# 1. Setup local connection
client = MongoClient("mongodb://localhost:27017/")
db = client["job_agent_db"]
collection = db["user_profile"]

# 2. Load the free embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 3. Your Resume (The "Single Chunk")
resume_text = """
Full Stack Developer with 3 years of experience. 
Tech Stack: Python, JavaScript, React, MongoDB. 
Preferred Role: Backend Engineer. 
Location: Hybrid (2 days in office).
"""

# 4. Convert text to a vector (list of numbers)
resume_vector = model.encode(resume_text).tolist()

# 5. Save to MongoDB
user_data = {
    "name": "User",
    "resume_content": resume_text,
    "resume_vector": resume_vector  # This is what the AI will 'search'
}

collection.update_one({"name": "User"}, {"$set": user_data}, upsert=True)

print("✅ Resume vectorized and stored in local MongoDB!")