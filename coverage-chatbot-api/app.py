"""
Day 3 skeleton — FastAPI backend for the coverage chatbot course.

Run from repo root or this folder:
  uvicorn coverage-chatbot-api.app:app --reload --port 8000
  # or, from inside this folder:
  uvicorn app:app --reload --port 8000
"""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Coverage Chatbot API",
    description="Backend skeleton for the healthcare coverage chatbot program.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check used by later Docker/K8s lessons."""
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "Coverage Chatbot API",
        "health": "/health",
        "docs": "/docs",
    }
