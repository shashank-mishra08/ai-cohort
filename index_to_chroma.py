"""
Day 9 — Load Day 6/7 knowledge base + embeddings into Chroma for retrieval.

- Batch upsert (~100) into collection coverage_kb
- Verify collection.count() == chunk count
- Test query: "Is physical therapy covered under the Silver plan?"
- Repeat with metadata filter (plan_type / section)

Usage:
  source .venv/bin/activate
  python3 index_to_chroma.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import chromadb
import numpy as np
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE = Path("knowledge_base.jsonl")
EMBEDDINGS_NPY = Path("embeddings.npy")
CHROMA_DIR = Path("chroma_db")
COLLECTION_NAME = "coverage_kb"
BATCH_SIZE = 100
MODEL_NAME = "all-MiniLM-L6-v2"
TEST_QUESTION = "Is physical therapy covered under the Silver plan?"

_model: SentenceTransformer | None = None


def get_embed_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embed model: {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed(text: str) -> list[float]:
    vec = get_embed_model().encode(text or "", normalize_embeddings=True)
    return vec.tolist()


def load_records() -> list[dict]:
    if not KNOWLEDGE_BASE.exists():
        raise SystemExit(f"Missing {KNOWLEDGE_BASE} (Day 6)")
    if not EMBEDDINGS_NPY.exists():
        raise SystemExit(f"Missing {EMBEDDINGS_NPY} (Day 7)")

    records = [
        json.loads(line)
        for line in KNOWLEDGE_BASE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    embeddings = np.load(EMBEDDINGS_NPY)
    if embeddings.shape[0] != len(records):
        raise SystemExit(
            f"Row mismatch: {len(records)} chunks vs embeddings {embeddings.shape}"
        )
    return records, embeddings


def normalize_plan_type(rec: dict) -> str:
    """Chroma-filter friendly plan label: Silver | Gold | Bronze | unknown."""
    raw = rec.get("plan_type")
    text = f"{raw or ''} {rec.get('text') or ''}".lower()

    if raw:
        r = str(raw).lower()
        if "silver" in r:
            return "Silver"
        if "gold" in r:
            return "Gold"
        if "bronze" in r:
            return "Bronze"

    # light text hints (structured plan sentences / mentions)
    if re.search(r"\bsilver(\s+hmo)?\b", text):
        return "Silver"
    if re.search(r"\bgold(\s+ppo)?\b", text):
        return "Gold"
    if re.search(r"\bbronze(\s+hmo)?\b", text):
        return "Bronze"
    return "unknown"


def to_chroma_metadata(rec: dict) -> dict:
    # Chroma metadata values must be str | int | float | bool (not None)
    plan_type = normalize_plan_type(rec)
    return {
        "chunk_id": str(rec.get("id") or ""),
        "source_file": str(rec.get("source_file") or "unknown"),
        "source_type": str(rec.get("source_type") or "unstructured"),
        "section": str(rec.get("section") or "coverage"),
        "plan_type": plan_type,
        "plan_type_raw": str(rec.get("plan_type") or "none"),
        "ingested_at": str(rec.get("ingested_at") or ""),
    }


def get_collection(reset: bool = True):
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR),
        settings=Settings(anonymized_telemetry=False),
    )
    if reset:
        # Fresh index so re-runs don't duplicate IDs
        try:
            client.delete_collection(COLLECTION_NAME)
            print(f"Deleted old collection: {COLLECTION_NAME}")
        except Exception:
            pass
        collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine", "day": "9"},
        )
        print(f"Created collection: {COLLECTION_NAME}")
    else:
        collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return client, collection


def batch_upsert(collection, records: list[dict], embeddings: np.ndarray) -> None:
    n = len(records)
    print(f"Upserting {n} chunks in batches of {BATCH_SIZE} ...")

    for start in range(0, n, BATCH_SIZE):
        end = min(start + BATCH_SIZE, n)
        batch_recs = records[start:end]
        batch_emb = embeddings[start:end]

        ids = [str(r.get("id") or f"chunk_{i+1:04d}") for i, r in enumerate(batch_recs, start=start)]
        documents = [str(r.get("text") or "") for r in batch_recs]
        metadatas = [to_chroma_metadata(r) for r in batch_recs]
        emb_list = batch_emb.astype(np.float32).tolist()

        collection.add(
            ids=ids,
            embeddings=emb_list,
            documents=documents,
            metadatas=metadatas,
        )
        print(f"  batch {start // BATCH_SIZE + 1}: added rows {start}..{end - 1} ({end - start} items)")


def print_query_results(title: str, result: dict) -> list[dict]:
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    rows = []
    ids = result.get("ids", [[]])[0]
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    dists = result.get("distances", [[]])[0]

    if not ids:
        print("(no results)")
        return rows

    for rank, (i, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), start=1):
        preview = (doc or "").replace("\n", " ")
        if len(preview) > 220:
            preview = preview[:220] + "..."
        print(f"\n#{rank} id={i}  distance={dist:.4f}")
        print(f"   section={meta.get('section')}  plan_type={meta.get('plan_type')}  source={meta.get('source_file')}")
        print(f"   text: {preview}")
        rows.append({"id": i, "distance": dist, "meta": meta, "doc": doc})
    return rows


def relevance_notes(rows: list[dict], question: str) -> None:
    print("\n--- Manual relevance notes ---")
    print(f"Question: {question}")
    if not rows:
        print("MISS: no chunks returned.")
        return

    silverish = sum(1 for r in rows if "silver" in json.dumps(r["meta"]).lower() or "silver" in (r["doc"] or "").lower())
    therapyish = sum(
        1
        for r in rows
        if re.search(r"physical therapy|physiotherapy|rehab|therapy", (r["doc"] or ""), re.I)
    )
    print(f"Results mentioning Silver: {silverish}/{len(rows)}")
    print(f"Results mentioning therapy/rehab-like terms: {therapyish}/{len(rows)}")
    print(
        "Note: synthetic SBC/template + Wikipedia knowledge may not contain a clear "
        "'physical therapy under Silver plan' clause. Retrieval can still return nearby "
        "coverage/plan language; treat plan-specific misses as expected data gaps, not only model failure."
    )


def main() -> None:
    print(f"Working dir: {Path.cwd()}")
    records, embeddings = load_records()
    print(f"Loaded {len(records)} chunks; embeddings shape {embeddings.shape}")

    # plan_type distribution after normalize
    from collections import Counter

    plans = Counter(normalize_plan_type(r) for r in records)
    print("Normalized plan_type counts:", dict(plans))

    _, collection = get_collection(reset=True)
    batch_upsert(collection, records, embeddings)

    count = collection.count()
    print("\n=== VERIFY COUNT ===")
    print(f"collection.count() = {count}")
    print(f"chunk count        = {len(records)}")
    if count != len(records):
        raise SystemExit("FAIL: count mismatch")
    print("PASS: collection count matches chunk count")

    # Step 4–5: raw test query
    q_emb = embed(TEST_QUESTION)
    raw = collection.query(
        query_embeddings=[q_emb],
        n_results=5,
        include=["documents", "metadatas", "distances"],
    )
    raw_rows = print_query_results(
        f'RAW query (no filter)\nQ: "{TEST_QUESTION}"',
        raw,
    )
    relevance_notes(raw_rows, TEST_QUESTION)

    # Step 6: metadata filter — plan_type Silver
    filtered = collection.query(
        query_embeddings=[q_emb],
        n_results=5,
        where={"plan_type": "Silver"},
        include=["documents", "metadatas", "distances"],
    )
    filt_rows = print_query_results(
        f'FILTERED query where={{"plan_type": "Silver"}}\nQ: "{TEST_QUESTION}"',
        filtered,
    )
    if filt_rows:
        bad = [r for r in filt_rows if r["meta"].get("plan_type") != "Silver"]
        if bad:
            print("FAIL: filter leaked non-Silver rows")
        else:
            print("\nPASS: all filtered rows have plan_type=Silver")
    else:
        print("\nNOTE: no Silver-tagged chunks matched (check metadata coverage).")

    # Bonus: section filter example
    claims = collection.query(
        query_embeddings=[embed("How do I file a claim?")],
        n_results=3,
        where={"section": "claims"},
        include=["documents", "metadatas", "distances"],
    )
    print_query_results('BONUS filter where={"section": "claims"}', claims)

    print("\n=== DAY 9 DONE ===")
    print("Chroma collection 'coverage_kb' is loaded and queryable.")
    print("Next days: hybrid retrieval / RAG answers on top of this index.")


if __name__ == "__main__":
    main()
