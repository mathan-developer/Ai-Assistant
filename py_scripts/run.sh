#!/usr/bin/env bash
#
# Helper for the RAG scripts. Always runs from the repo root so the
# dataset paths resolve, and uses the project virtualenv.
#
# Usage:
#   ./py_scripts/run.sh embeddings   # (re)generate dataset/embeddings.json
#   ./py_scripts/run.sh search       # interactive vector search
#   ./py_scripts/run.sh rag          # interactive RAG (needs Ollama running)
#   ./py_scripts/run.sh api          # serve the FastAPI app on :8000
#   ./py_scripts/run.sh install      # create venv + install requirements

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PY="$SCRIPT_DIR/.venv/bin/python"

cd "$REPO_ROOT"

cmd="${1:-help}"

case "$cmd" in
  install)
    python3.11 -m venv "$SCRIPT_DIR/.venv"
    "$VENV_PY" -m pip install --upgrade pip
    "$VENV_PY" -m pip install -r "$SCRIPT_DIR/requirements.txt"
    ;;
  embeddings)
    "$VENV_PY" py_scripts/scripts/generate_embeddings.py
    ;;
  search)
    "$VENV_PY" py_scripts/scripts/vector_search.py
    ;;
  rag)
    "$VENV_PY" py_scripts/backend/rag_pipeline.py
    ;;
  api)
    "$VENV_PY" -m uvicorn py_scripts.backend.api_server:app --reload --host 0.0.0.0 --port 8000
    ;;
  *)
    echo "Usage: $0 {install|embeddings|search|rag|api}"
    exit 1
    ;;
esac
