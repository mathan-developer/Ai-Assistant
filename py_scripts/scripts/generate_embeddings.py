from sentence_transformers import SentenceTransformer
import json

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# load dataset
with open("dataset/questions.json", "r") as f:
    data = json.load(f)

embeddings = []

for item in data:

    text = f"""
    Problem: {item['question']}
    Description: {item['description']}
    Hint: {item['hint']}
    """

    vector = model.encode(text)

    embeddings.append({
        "id": item["id"],
        "question": item["question"],
        "embedding": vector.tolist()
    })

# save embeddings
with open("dataset/embeddings.json", "w") as f:
    json.dump(embeddings, f)

print("Embeddings generated successfully!")