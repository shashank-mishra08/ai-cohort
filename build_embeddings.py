"""
Day 7 — Generate embeddings for every knowledge_base.jsonl chunk.

Free path (recommended): sentence-transformers / all-MiniLM-L6-v2
Outputs:
  embeddings.npy      — one row per chunk (same order as JSONL)
  embeddings_2d.png   — PCA scatter colored by section
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer

KNOWLEDGE_BASE = Path("knowledge_base.jsonl")
EMBEDDINGS_NPY = Path("embeddings.npy")
EMBEDDINGS_PNG = Path("embeddings_2d.png")
MODEL_NAME = "all-MiniLM-L6-v2"

# Fixed colors for Day 7 section labels
SECTION_COLORS = {
    "coverage": "#1f77b4",
    "exclusions": "#d62728",
    "claims": "#2ca02c",
    "enrollment": "#ff7f0e",
}
DEFAULT_COLOR = "#7f7f7f"

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME} ...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Model ready.")
    return _model


def embed(text: str) -> list[float]:
    """embed(text) -> vector  (dense meaning representation)."""
    model = get_model()
    vec = model.encode(text or "", normalize_embeddings=True)
    return vec.tolist()


def embed_batch(texts: list[str], batch_size: int = 64) -> np.ndarray:
    model = get_model()
    vectors = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    return np.asarray(vectors, dtype=np.float32)


def load_chunks(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"Missing {path} — run Day 6 first (build_knowledge_base.py).")
    records: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            records.append(json.loads(line))
    if not records:
        raise SystemExit(f"{path} is empty.")
    return records


def plot_2d(embeddings: np.ndarray, sections: list[str], out_path: Path) -> None:
    """PCA to 2D + scatter colored by section."""
    n = embeddings.shape[0]
    if n < 2:
        raise SystemExit("Need at least 2 chunks to plot PCA.")

    n_components = 2 if n >= 2 else 1
    coords = PCA(n_components=n_components, random_state=42).fit_transform(embeddings)
    if n_components == 1:
        coords = np.column_stack([coords[:, 0], np.zeros(n)])

    plt.figure(figsize=(10, 7))
    # Plot each section so the legend is clean
    unique_sections = sorted(set(sections))
    for section in unique_sections:
        idxs = [i for i, s in enumerate(sections) if s == section]
        color = SECTION_COLORS.get(section.lower(), DEFAULT_COLOR)
        plt.scatter(
            coords[idxs, 0],
            coords[idxs, 1],
            c=color,
            label=section.title(),
            alpha=0.75,
            s=36,
            edgecolors="white",
            linewidths=0.3,
        )

    plt.title("Day 7 — Knowledge base embeddings (PCA 2D)\nmodel: all-MiniLM-L6-v2")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(title="Section", loc="best", framealpha=0.9)
    plt.grid(True, alpha=0.25)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()
    print(f"Saved plot: {out_path.resolve()}")


def main() -> None:
    print(f"Working dir: {Path.cwd()}")
    records = load_chunks(KNOWLEDGE_BASE)
    texts = [str(r.get("text") or "") for r in records]
    sections = [str(r.get("section") or "unknown").lower() for r in records]

    print(f"Chunks loaded: {len(records)}")
    print("Section counts:", dict(Counter(sections)))

    embeddings = embed_batch(texts)
    if embeddings.shape[0] != len(records):
        raise SystemExit("Embedding row count does not match chunk count.")

    np.save(EMBEDDINGS_NPY, embeddings)
    print(f"Saved: {EMBEDDINGS_NPY.resolve()}")
    print(f"Shape: {embeddings.shape}  (rows=chunks, cols=dimensions)")
    print(f"Dtype: {embeddings.dtype}")

    # Quick sanity: cosine sim of first chunk with itself ~ 1.0 (normalized)
    self_sim = float(np.dot(embeddings[0], embeddings[0]))
    print(f"Sanity self-similarity (chunk 0): {self_sim:.4f}")

    plot_2d(embeddings, sections, EMBEDDINGS_PNG)

    # Tiny clustering check: average pairwise cosine within vs across sections
    def mean_intra(section: str) -> float | None:
        idxs = [i for i, s in enumerate(sections) if s == section]
        if len(idxs) < 2:
            return None
        vecs = embeddings[idxs]
        # sample to keep it cheap
        if len(idxs) > 40:
            rng = np.random.default_rng(42)
            pick = rng.choice(len(idxs), size=40, replace=False)
            vecs = vecs[pick]
        sims = vecs @ vecs.T
        n = sims.shape[0]
        # exclude diagonal
        total = (sims.sum() - n) / (n * (n - 1))
        return float(total)

    print("\n=== Rough clustering check (mean intra-section cosine) ===")
    for section in sorted(set(sections)):
        score = mean_intra(section)
        if score is not None:
            print(f"  {section:12s}: {score:.4f}")

    print("\nDone. Deliverables: embeddings.npy + embeddings_2d.png")
    print("Try: python3 -c \"from build_embeddings import embed; print(len(embed('deductible')))\"")


if __name__ == "__main__":
    main()
