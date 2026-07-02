import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.retrieval import ask_llm, ask_llm_stream, search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


def build_prompt(question: str) -> tuple[str, str]:
    results = search(question)
    context = "\n".join(q for q, _ in results)

    prompt = f"""
You are a technical interviewer.

Context:
{context}

Question:
{question}

Explain short and clearly.
"""
    return prompt, context


@app.post("/ask")
def ask_question(q: Question):
    prompt, context = build_prompt(q.question)

    try:
        answer = ask_llm(prompt)
    except RuntimeError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {"answer": answer, "context": context}


@app.post("/ask/stream")
def ask_question_stream(q: Question):
    prompt, _ = build_prompt(q.question)

    def token_generator():
        try:
            for token in ask_llm_stream(prompt):
                yield token
        except RuntimeError as exc:
            yield f"\n[error] {exc}"

    return StreamingResponse(token_generator(), media_type="text/plain; charset=utf-8")
