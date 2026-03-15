import json
import numpy as np
from sentence_transformers import SentenceTransformer

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# load embeddings
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


query = input("Ask a question: ")

results = search(query)

print("\nTop Matches:\n")

for r in results:
    print(r)