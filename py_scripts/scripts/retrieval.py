import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import requests

MODEL_NAME = "all-MiniLM-L6-v2"

DATASET_DIR = "/Users/mathan/Documents/Projects/Android Projects/AiApplication/dataset"
QUESTIONS_PATH = f"{DATASET_DIR}/questions.json"
EMBEDDINGS_PATH = f"{DATASET_DIR}/embeddings.json"

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL ="mistral" #"qwen3:14b"

# Keep the model resident between requests to avoid cold-start reloads, and
# cap the answer length so generation time stays bounded.
KEEP_ALIVE = "30m"
LLM_OPTIONS = {"num_predict": 256}


@lru_cache(maxsize=1)
def get_model():
    # Imported lazily so scripts that only read the dataset don't pay the
    # cost of loading torch/transformers until an encode is actually needed.
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


@lru_cache(maxsize=1)
def _load_index():
    with open(EMBEDDINGS_PATH, "r") as f:
        data = json.load(f)

    questions = [item["question"] for item in data]
    matrix = np.array([item["embedding"] for item in data], dtype=np.float32)

    # Pre-normalize once so search becomes a single matrix-vector product.
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1e-12
    matrix = matrix / norms

    return questions, matrix


def search(query, top_k=3):
    questions, matrix = _load_index()

    query_embedding = get_model().encode(query, normalize_embeddings=True)

    scores = matrix @ query_embedding
    top_idx = np.argsort(scores)[::-1][:top_k]

    return [(questions[i], float(scores[i])) for i in top_idx]


def ask_llm(prompt, timeout=120):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": False,
                "keep_alive": KEEP_ALIVE,
                "options": LLM_OPTIONS,
            },
            timeout=timeout,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    data = response.json()
    if "response" not in data:
        raise RuntimeError(f"Unexpected LLM response: {data}")

    return data["response"]


def ask_llm_stream(prompt, timeout=120):
    """Yield answer tokens from Ollama as they are generated (NDJSON stream)."""
    try:
        with requests.post(
            OLLAMA_URL,
            json={
                "model": LLM_MODEL,
                "prompt": prompt,
                "stream": True,
                "keep_alive": KEEP_ALIVE,
                "options": LLM_OPTIONS,
            },
            timeout=timeout,
            stream=True,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                token = chunk.get("response", "")
                if token:
                    yield token
                if chunk.get("done"):
                    break
    except requests.RequestException as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc
