"""
Day 5 — scrape a public text-heavy webpage and save clean article text.

Uses requests + BeautifulSoup. Removes nav/footer/script/style/ads-like chrome,
keeps main readable text, writes raw_text/webpage.txt.
"""

from __future__ import annotations

import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

# Text-heavy public page (Wikipedia works reliably for this exercise)
URL = "https://en.wikipedia.org/wiki/Health_insurance_in_the_United_States"

OUTPUT_DIR = Path("raw_text")
OUTPUT_FILE = OUTPUT_DIR / "webpage.txt"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    # Drop empty lines and obvious leftover noise
    kept: list[str] = []
    for line in lines:
        s = line.strip()
        if not s:
            if kept and kept[-1] != "":
                kept.append("")
            continue
        kept.append(s)
    cleaned = re.sub(r"\n{3,}", "\n\n", "\n".join(kept))
    return cleaned.strip() + "\n"


def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Remove unwanted chrome
    for tag in soup(
        [
            "nav",
            "footer",
            "header",
            "script",
            "style",
            "noscript",
            "aside",
            "form",
            "button",
            "iframe",
            "svg",
        ]
    ):
        tag.decompose()

    # Common Wikipedia / site chrome
    for selector in [
        "#mw-navigation",
        "#mw-panel",
        "#mw-head",
        "#footer",
        ".vector-header-container",
        ".vector-toc",
        ".navbox",
        ".mbox-small",
        ".reference",
        ".mw-editsection",
        "table.infobox",
        "table.sidebar",
    ]:
        for el in soup.select(selector):
            el.decompose()

    # Prefer main content region when present
    main = (
        soup.select_one("#mw-content-text")
        or soup.select_one("main")
        or soup.select_one("article")
        or soup.body
        or soup
    )

    # Prefer paragraphs for cleaner article text
    paragraphs = [p.get_text(" ", strip=True) for p in main.find_all("p")]
    paragraphs = [p for p in paragraphs if p and len(p) > 40]
    if paragraphs:
        return clean_text("\n\n".join(paragraphs))

    return clean_text(main.get_text("\n", strip=True))


def main() -> None:
    print(f"Fetching: {URL}")
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()

    text = extract_main_text(response.text)
    if not text.strip():
        raise SystemExit(
            "Empty scrape result. Try a simpler Wikipedia/FAQ URL in scrape.py."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    print(f"Saved: {OUTPUT_FILE.resolve()} ({len(text)} chars)")
    print("Preview (first 400 chars):")
    print(text[:400])
    print("Done.")


if __name__ == "__main__":
    main()
