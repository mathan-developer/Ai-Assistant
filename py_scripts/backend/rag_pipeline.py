import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from retrieval import ask_llm, search

query = input("Ask your question: ")

results = search(query)

context = "\n".join(question for question, _ in results)

prompt = f"""
You are a technical interviewer.

Context:
{context}

Question:
{query}

Explain clearly.
"""

try:
    answer = ask_llm(prompt)
except RuntimeError as exc:
    print(f"\nError: {exc}")
    sys.exit(1)

print("\nAI Answer:\n")
print(answer)
print("\nRetrieved Context:")
print(context)
