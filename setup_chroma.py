"""
Day 8 — Stand up a persistent local Chroma instance.

Creates (or reopens) a collection named: coverage_kb

Usage:
  source .venv/bin/activate
  python3 setup_chroma.py
"""

from __future__ import annotations

from pathlib import Path

import chromadb
from chromadb.config import Settings

# Persistent on-disk store (survives restarts)
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "coverage_kb"


def get_client() -> chromadb.ClientAPI:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )


def get_or_create_coverage_kb(client: chromadb.ClientAPI):
    """Mission step: client.create_collection('coverage_kb') — safe if already exists."""
    existing = {c.name for c in client.list_collections()}
    if COLLECTION_NAME in existing:
        collection = client.get_collection(COLLECTION_NAME)
        created = False
    else:
        # Explicit create as required by the mission wording
        collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={
                "description": "Healthcare coverage knowledge base vectors (Day 8+)",
                "hnsw:space": "cosine",
            },
        )
        created = True
    return collection, created


def main() -> None:
    print(f"Working dir: {Path.cwd()}")
    print(f"Chroma persistent path: {CHROMA_DIR.resolve()}")

    client = get_client()
    collection, created = get_or_create_coverage_kb(client)

    action = "CREATED" if created else "REOPENED"
    count = collection.count()

    print(f"\n=== Chroma status ===")
    print(f"Collection: {collection.name}  ({action})")
    print(f"Vectors currently stored: {count}  (empty is OK on Day 8)")
    print(f"All collections: {[c.name for c in client.list_collections()]}")

    # Heartbeat-style checks so we know the instance is alive
    heartbeat = client.heartbeat()
    print(f"Client heartbeat: {heartbeat}")

    print("\nDone. Local Chroma is ready for Day 9 (load embeddings into coverage_kb).")
    print("Tip: keep the chroma_db/ folder; do not delete it between days.")


if __name__ == "__main__":
    main()
