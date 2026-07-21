"""
Day 2 — Verify Ollama is installed, a coding model is available, and the local API works.

Usage:
  python3 day02_verify_ollama.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

API = "http://localhost:11434"
PREFERRED = [
    "qwen2.5-coder:7b",
    "qwen2.5-coder:3b",
    "qwen2.5-coder:14b",
]


def ok(msg: str) -> None:
    print(f"PASS  {msg}")


def fail(msg: str) -> None:
    print(f"FAIL  {msg}")


def warn(msg: str) -> None:
    print(f"WARN  {msg}")


def main() -> int:
    print("=== Day 2 Ollama verification ===\n")
    errors = 0

    # 1) CLI installed
    path = shutil.which("ollama")
    if not path:
        fail("ollama CLI not found. Install from https://ollama.com and reopen Terminal.")
        return 1
    ok(f"ollama CLI found at {path}")

    # 2) version
    try:
        ver = subprocess.check_output(["ollama", "--version"], text=True, stderr=subprocess.STDOUT)
        ok(f"version: {ver.strip()}")
    except Exception as exc:
        fail(f"ollama --version failed: {exc}")
        errors += 1

    # 3) API up
    try:
        with urllib.request.urlopen(API, timeout=5) as resp:
            body = resp.read().decode("utf-8", errors="replace").strip()
        if "running" in body.lower() or body:
            ok(f"API {API} responded: {body[:80]}")
        else:
            fail(f"API {API} empty response — open the Ollama app from Applications")
            errors += 1
    except urllib.error.URLError as exc:
        fail(f"API not reachable at {API}: {exc}")
        warn("Open /Applications/Ollama.app (menu-bar icon should appear), wait 10s, re-run.")
        errors += 1
        return 1

    # 4) list models
    try:
        with urllib.request.urlopen(f"{API}/api/tags", timeout=10) as resp:
            data = json.loads(resp.read().decode())
        models = [m.get("name", "") for m in data.get("models", [])]
    except Exception as exc:
        fail(f"Could not list models: {exc}")
        return 1

    if not models:
        fail("No models pulled yet.")
        warn("For 8GB RAM:  ollama pull qwen2.5-coder:3b")
        warn("For 16GB RAM: ollama pull qwen2.5-coder:7b")
        return 1

    ok("models installed:")
    for name in models:
        print(f"      - {name}")

    pick = next((m for m in PREFERRED if m in models), models[0])
    ok(f"using model for smoke test: {pick}")

    # 5) generate
    payload = json.dumps(
        {
            "model": pick,
            "prompt": "Write only: def reverse_string(s): return s[::-1]",
            "stream": False,
            "options": {"num_predict": 60},
        }
    ).encode()
    req = urllib.request.Request(
        f"{API}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            out = json.loads(resp.read().decode())
        text = (out.get("response") or "").strip()
        if text:
            ok("local generation works")
            print("------ model reply (truncated) ------")
            print(text[:400])
            print("----------------------------------")
        else:
            fail("model returned empty text")
            errors += 1
    except Exception as exc:
        fail(f"generation failed: {exc}")
        errors += 1

    print("\n=== VS Code wiring (manual check) ===")
    print("Option A — GitHub Copilot Free:")
    print("  Extensions → GitHub Copilot → Install → Sign in")
    print("  Chat panel → model dropdown → Manage Models → Ollama → select your model")
    print("Option B — Cline (no GitHub):")
    print("  Extensions → Cline (saoudrizwan) → Settings → API Provider: Ollama")
    print("  Base URL: http://localhost:11434 → pick model")
    print("\nDeliverable: Ollama + model + VS Code chat using local model (works offline).")

    if errors:
        print(f"\nRESULT: {errors} issue(s) — fix FAIL lines above.")
        return 1
    print("\nRESULT: Ollama Day 2 core checks PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
