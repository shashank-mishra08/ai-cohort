"""
Day 6 — Build knowledge_base.jsonl from Day 5 raw_text files + Day 4 plan rows.

- RecursiveCharacterTextSplitter (chunk_size=500, chunk_overlap=50)
- Prefer splitting on section headers / paragraphs so exclusions & claims stay intact
- Each JSONL line: id, text, source_file, source_type, section, plan_type, ingested_at
"""

from __future__ import annotations

import csv
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

RAW_TEXT_DIR = Path("raw_text")
PLANS_CSV = Path("data/plans.csv")
OUTPUT_FILE = Path("knowledge_base.jsonl")

# Prefer large structural breaks first so sections stay together when possible.
# Section headers for benefits / claims / enrollment docs rank highest.
SEPARATORS = [
    "\n\n## ",
    "\n\n# ",
    "\n\n===",
    "\n\n--- Page",
    "\n\n1. ",
    "\n\n2. ",
    "\n\n3. ",
    "\n\n4. ",
    "\n\n5. ",
    "\n\nWhat is not covered",
    "\n\nExclusions",
    "\n\nExcluded",
    "\n\nCovered services",
    "\n\nCoverage",
    "\n\nClaims",
    "\n\nHow to File a Claim",
    "\n\nAppeals",
    "\n\n",
    "\n",
    ". ",
    " ",
    "",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_section_for_file(filename: str) -> str:
    name = filename.lower()
    if "claim" in name:
        return "claims"
    if "enroll" in name:
        return "enrollment"
    if "benefit" in name or "sbc" in name or "coverage" in name:
        return "coverage"
    if "webpage" in name or "web" in name:
        return "coverage"
    return "coverage"


def infer_section(text: str, fallback: str) -> str:
    low = text.lower()
    # Order matters: more specific labels first
    rules = [
        ("exclusions", [r"\bexclusion", r"\bnot covered\b", r"\bdoes not cover\b", r"\bexcluded\b"]),
        ("claims", [r"\bclaim", r"\beob\b", r"\bappeal", r"\bgrievance", r"\badjudicat"]),
        ("enrollment", [r"\benroll", r"\beffective date", r"\bdependent", r"\bmember full name"]),
        ("coverage", [r"\bdeductible", r"\bcopay", r"\bcoinsurance", r"\bpremium", r"\bcovered service", r"\bbenefit"]),
    ]
    for section, patterns in rules:
        for pat in patterns:
            if re.search(pat, low):
                return section
    return fallback


def infer_plan_type(text: str) -> str | None:
    low = text.lower()
    for label in ("gold ppo", "silver hmo", "bronze hmo", "ppo", "hmo"):
        if label in low:
            return label.upper() if label in ("ppo", "hmo") else label.title()
    return None


def make_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
        separators=SEPARATORS,
        keep_separator=True,
    )


def load_raw_text_files() -> list[Path]:
    if not RAW_TEXT_DIR.exists():
        raise SystemExit(f"Missing folder: {RAW_TEXT_DIR}/ (run Day 5 extraction first)")
    files = sorted(RAW_TEXT_DIR.glob("*.txt"))
    if not files:
        raise SystemExit(f"No .txt files found in {RAW_TEXT_DIR}/")
    return files


def chunk_document(path: Path, splitter: RecursiveCharacterTextSplitter, ingested_at: str) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if not text:
        return []

    fallback_section = default_section_for_file(path.name)
    pieces = splitter.split_text(text)
    records: list[dict] = []

    for piece in pieces:
        chunk = piece.strip()
        if not chunk:
            continue
        # Avoid tiny leftover fragments
        if len(chunk) < 40 and len(pieces) > 1:
            continue
        records.append(
            {
                "id": None,  # filled later for global uniqueness
                "text": chunk,
                "source_file": path.name,
                "source_type": "unstructured",
                "section": infer_section(chunk, fallback_section),
                "plan_type": infer_plan_type(chunk),
                "ingested_at": ingested_at,
            }
        )
    return records


def chunk_plans(ingested_at: str) -> list[dict]:
    """One structured chunk per plan row (Day 4 plans table export)."""
    path = PLANS_CSV if PLANS_CSV.exists() else Path("plans.csv")
    if not path.exists():
        print(f"Note: no plans CSV at {PLANS_CSV}; skipping structured plan chunks.")
        return []

    records: list[dict] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            plan_name = (row.get("plan_name") or "").strip()
            premium = row.get("monthly_premium", "")
            deductible = row.get("annual_deductible", "")
            copay = row.get("copay_pct", "")
            coverage_type = (row.get("coverage_type") or "").strip()
            network = (row.get("network_tier") or "").strip()
            plan_id = (row.get("plan_id") or "").strip()

            text = (
                f"{plan_name}: ${premium}/month premium, ${deductible} deductible, "
                f"{copay}% coinsurance/copay, network: {network or 'national'}, "
                f"coverage type: {coverage_type}, plan_id: {plan_id}."
            )
            records.append(
                {
                    "id": None,
                    "text": text,
                    "source_file": path.name,
                    "source_type": "structured",
                    "section": "coverage",
                    "plan_type": plan_name or coverage_type or None,
                    "ingested_at": ingested_at,
                }
            )
    return records


def assign_ids(records: list[dict]) -> None:
    for i, rec in enumerate(records, start=1):
        rec["id"] = f"chunk_{i:04d}"


def write_jsonl(records: list[dict], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def sanity_check(records: list[dict], sample_n: int = 5) -> None:
    print("\n=== SANITY CHECK: random sample chunks ===")
    if not records:
        print("No records to sample.")
        return
    sample = random.sample(records, k=min(sample_n, len(records)))
    for rec in sample:
        text = rec["text"]
        ends_mid_word = bool(re.search(r"[A-Za-z0-9]$", text)) and len(text) >= 480
        print("-" * 60)
        print(
            f"id={rec['id']} | source={rec['source_file']} | "
            f"type={rec['source_type']} | section={rec['section']} | "
            f"plan_type={rec.get('plan_type')} | chars={len(text)}"
        )
        preview = text if len(text) <= 320 else text[:320] + "..."
        print(preview)
        if "exclusion" in text.lower() or "not covered" in text.lower():
            print("[note] exclusion-related chunk — review that clause looks intact")
        if ends_mid_word:
            print("[warn] chunk may end mid-sentence; separators/overlap usually mitigate this")


def main() -> None:
    ingested_at = utc_now_iso()
    splitter = make_splitter()

    print(f"Working dir: {Path.cwd()}")
    print(f"Reading text from: {RAW_TEXT_DIR.resolve()}")
    print(f"Chunk size=500, overlap=50")

    all_records: list[dict] = []

    for path in load_raw_text_files():
        docs = chunk_document(path, splitter, ingested_at)
        print(f"  {path.name}: {len(docs)} chunks")
        all_records.extend(docs)

    plan_chunks = chunk_plans(ingested_at)
    print(f"  plans structured: {len(plan_chunks)} chunks")
    all_records.extend(plan_chunks)

    assign_ids(all_records)
    write_jsonl(all_records, OUTPUT_FILE)

    print("\n=== TOTAL CHUNKS ===")
    print(len(all_records))
    print(f"Saved: {OUTPUT_FILE.resolve()}")

    # Section / source summary
    by_section: dict[str, int] = {}
    by_source: dict[str, int] = {}
    for rec in all_records:
        by_section[rec["section"]] = by_section.get(rec["section"], 0) + 1
        by_source[rec["source_file"]] = by_source.get(rec["source_file"], 0) + 1
    print("By section:", by_section)
    print("By source:", by_source)

    sanity_check(all_records, sample_n=5)
    print("\nDone. Deliverable ready: knowledge_base.jsonl")


if __name__ == "__main__":
    main()
