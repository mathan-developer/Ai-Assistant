import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval import search

query = input("Ask a question: ")

results = search(query)

print("\nTop Matches:\n")

for question, score in results:
    print(f"{score:.4f}  {question}")
