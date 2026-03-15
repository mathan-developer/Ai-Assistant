from fastapi import FastAPI
from pydantic import BaseModel
import json
import numpy as np
import requests
from sentence_transformers import SentenceTransformer

app = FastAPI()

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("dataset/embeddings.json", "r") as f:
    embeddings_data = json.load(f)


class Question(BaseModel):
    question: str


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


@app.post("/ask")
def ask_question(q: Question):

    results = search(q.question)

    context = "\n".join([r[0] for r in results])

    prompt = f"""
You are a technical interviewer.

Context:
{context}

Question:
{q.question}

Explain short and clearly.
"""

    answer = ask_llm(prompt)

    return {"answer": answer}