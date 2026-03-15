import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("dataset/embeddings.json", "r") as f:
    embeddings_data = json.load(f)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, top_k=3):

    query_embedding = model.encode(query)

    scores = []

    for item in embeddings_data:
        stored_embedding = np.array(item["embedding"])
        similarity = cosine_similarity(query_embedding, stored_embedding)

        scores.append((item["question"], similarity))

    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:top_k]

def ask_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

query = input("Ask your question: ")

results = search(query)

context = "\n".join([r[0] for r in results])

prompt = f"""
You are a technical interviewer.

Context:
{context}

Question:
{query}

Explain clearly.
"""

answer = ask_llm(prompt)

print("\nAI Answer:\n")
print(answer)
print("\nRetrieved Context:")
print(context)