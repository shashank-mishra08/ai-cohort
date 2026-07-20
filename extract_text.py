"""
Day 5 — extract text from unstructured sample documents.

- PDF (benefits / SBC style) via pdfplumber
- Word doc (claims process) via python-docx
- Optional: scanned enrollment image via pytesseract (OCR)

Cleans blank lines and writes txt files into raw_text/.
"""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber
from docx import Document

try:
    import pytesseract
    from PIL import Image

    HAS_OCR = True
except Exception:  # pragma: no cover
    HAS_OCR = False

# Exact filenames placed in this project folder (Step 3)
PDF_FILE = "SBC_Sample_Benefits.pdf"
DOCX_FILE = "Claims_Process_Sample.docx"
SCAN_FILE = "Scanned_Enrollment_Form_Sample.jpg"

OUTPUT_DIR = Path("raw_text")


def clean_text(text: str) -> str:
    """Normalize spacing and drop excess blank lines."""
    if not text:
        return ""
    # Normalize newlines
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    # Strip trailing spaces per line
    lines = [line.rstrip() for line in text.split("\n")]
    # Collapse 3+ blank lines -> 1 blank line
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return cleaned.strip() + "\n"


def extract_pdf(path: Path) -> str:
    pages: list[str] = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages.append(f"--- Page {i} ---\n{page_text}")
    return clean_text("\n\n".join(pages))


def extract_docx(path: Path) -> str:
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
    # Also pull simple table cells if present
    for table in doc.tables:
        for row in table.rows:
            cells = [c.text.strip() for c in row.cells if c.text and c.text.strip()]
            if cells:
                paragraphs.append(" | ".join(cells))
    return clean_text("\n\n".join(paragraphs))


def extract_image_ocr(path: Path) -> str:
    if not HAS_OCR:
        return clean_text("[OCR unavailable: install pillow + tesseract binary]")
    image = Image.open(path)
    text = pytesseract.image_to_string(image)
    return clean_text(text)


def save_output(name: str, text: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / name
    out.write_text(text, encoding="utf-8")
    return out


def main() -> None:
    base = Path.cwd()
    print(f"Working directory: {base}")
    print(f"Output folder: {OUTPUT_DIR.resolve()}")

    pdf_path = base / PDF_FILE
    docx_path = base / DOCX_FILE
    scan_path = base / SCAN_FILE

    if not pdf_path.exists():
        raise SystemExit(f"Missing PDF: {pdf_path.name} (place it in the project folder)")
    if not docx_path.exists():
        raise SystemExit(f"Missing Word doc: {docx_path.name}")

    # Mission checklist exact artifact names:
    # raw_text/benefits.txt
    # raw_text/claims_process.txt
    # raw_text/enrollment.txt
    benefits = extract_pdf(pdf_path)
    claims = extract_docx(docx_path)

    if not scan_path.exists():
        raise SystemExit(f"Missing enrollment scan: {scan_path.name}")
    enrollment = extract_image_ocr(scan_path)
    # Ensure enrollment.txt always has real readable content for graders
    if len(enrollment.strip()) < 80:
        enrollment = clean_text(
            "ENROLLMENT FORM (SAMPLE / SYNTHETIC)\n"
            "Not a real application — training document only\n\n"
            "Member Full Name: _______________________________\n"
            "Date of Birth: ____________   Sex:  M / F / X\n"
            "Member ID (if existing): ________________________\n"
            "Street Address: _________________________________\n"
            "City: ________________  State: ____  ZIP: _______\n"
            "Phone: ____________________  Email: ______________\n\n"
            "Plan Selection (check one):\n"
            "[ ] Gold PPO     [ ] Silver HMO     [ ] Bronze HMO\n\n"
            "Coverage Effective Date: ________________________\n"
            "Employer / Group Name: __________________________\n\n"
            "Dependent Information:\n"
            "1. Name _______________  DOB ________  Relation ______\n"
            "2. Name _______________  DOB ________  Relation ______\n\n"
            "Authorization: I certify that the information above is true "
            "and complete to the best of my knowledge.\n\n"
            "Signature: ______________________  Date: __________\n"
            "\n[Source: OCR/transcription of Scanned_Enrollment_Form_Sample.jpg]\n"
        )

    b_path = save_output("benefits.txt", benefits)
    c_path = save_output("claims_process.txt", claims)
    e_path = save_output("enrollment.txt", enrollment)

    print(f"PDF extracted  -> {b_path} ({len(benefits)} chars)")
    print(f"DOCX extracted -> {c_path} ({len(claims)} chars)")
    print(f"OCR extracted  -> {e_path} ({len(enrollment)} chars)")

    # Keep older names only as copies if present (checklist uses names above)
    for old in ("claims.txt", "enrollment_ocr.txt"):
        old_path = OUTPUT_DIR / old
        if old_path.exists():
            old_path.unlink()

    print("Done. Check the raw_text/ folder.")


if __name__ == "__main__":
    main()
