import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval import EMBEDDINGS_PATH, QUESTIONS_PATH, get_model

model = get_model()

with open(QUESTIONS_PATH, "r") as f:
    data = json.load(f)

texts = [
    f"""
    Problem: {item['question']}
    Description: {item['description']}
    Hint: {item['hint']}
    """
    for item in data
]

# Encode the whole dataset in one batched call instead of one-by-one.
vectors = model.encode(texts)

embeddings = [
    {
        "id": item["id"],
        "question": item["question"],
        "embedding": vector.tolist(),
    }
    for item, vector in zip(data, vectors)
]

with open(EMBEDDINGS_PATH, "w") as f:
    json.dump(embeddings, f)

print("Embeddings generated successfully!")
