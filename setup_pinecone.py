"""
Day 8 — Create an empty Pinecone serverless index (optional cloud path).

Requires a free Pinecone account + API key:
  1. Sign up: https://app.pinecone.io/ (free tier, no credit card)
  2. Create an API key in the console
  3. Export it, then run this script:

       export PINECONE_API_KEY="your-key-here"
       python3 setup_pinecone.py

Creates an empty index ready for later upserts (Day 9+).
If no API key is set, prints setup instructions and exits without failing the Day 8 Chroma path.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

INDEX_NAME = "coverage-kb"
# Match Day 7 Sentence-Transformers model dimension (all-MiniLM-L6-v2)
DIMENSION = 384
METRIC = "cosine"
CLOUD = "aws"
REGION = "us-east-1"


def main() -> None:
    print(f"Working dir: {Path.cwd()}")
    api_key = os.environ.get("PINECONE_API_KEY", "").strip()

    if not api_key:
        print(
            """
=== Pinecone API key not found ===

Day 8 still requires YOU to create a free Pinecone account (one-time, in browser):
  1. Open https://app.pinecone.io/ and sign up (free tier, no credit card).
  2. In the console, create / copy an API key.
  3. In Terminal (same session):

       export PINECONE_API_KEY="paste-your-key-here"
       source .venv/bin/activate
       python3 setup_pinecone.py

Optional: create a Serverless index named "coverage-kb" in the dashboard instead
(dimension 384, metric cosine) — same result as this script.

This script will create an EMPTY index only (no vectors yet — that is Day 9).
"""
        )
        sys.exit(0)

    try:
        from pinecone import Pinecone, ServerlessSpec
    except ImportError:
        print("Install pinecone first: pip install pinecone")
        sys.exit(1)

    pc = Pinecone(api_key=api_key)
    existing = {idx["name"] for idx in pc.list_indexes()}

    if INDEX_NAME in existing:
        print(f"Index already exists: {INDEX_NAME}")
    else:
        print(f"Creating serverless index: {INDEX_NAME} (dim={DIMENSION}, metric={METRIC}) ...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(cloud=CLOUD, region=REGION),
        )
        # Wait until ready
        for _ in range(60):
            desc = pc.describe_index(INDEX_NAME)
            status = getattr(desc, "status", None) or {}
            ready = status.get("ready") if isinstance(status, dict) else getattr(status, "ready", False)
            if ready:
                break
            time.sleep(2)
        print(f"Created index: {INDEX_NAME}")

    desc = pc.describe_index(INDEX_NAME)
    print("=== Pinecone status ===")
    print(f"Name: {INDEX_NAME}")
    print(f"Dimension: {DIMENSION}")
    print(f"Metric: {METRIC}")
    print(f"Description: {desc}")
    print("\nDone. Empty Pinecone index is ready (vectors come on Day 9+).")


if __name__ == "__main__":
    main()
