"""
Day 3 — command-line chatbot against your local Ollama model.

Usage:
  # Terminal 1: Ollama app running (menu bar icon)
  cd /Users/shashank/projects/my-first-app
  source .venv/bin/activate
  pip install ollama
  python3 chatbot.py

Type 'quit' to exit.

This machine (8 GB RAM) uses qwen2.5-coder:3b per the course guide.
"""

from __future__ import annotations

import sys

try:
    import ollama
except ImportError:
    print("Install ollama package: pip install ollama")
    sys.exit(1)

# 8 GB RAM → qwen2.5-coder:3b  |  16 GB → :7b  |  32 GB+ → :14b
MODEL = "qwen2.5-coder:3b"


def main() -> None:
    history: list[dict[str, str]] = []
    print("Local chatbot (Ollama) — type 'quit' to exit")
    print(f"Model: {MODEL}")
    print("API: http://localhost:11434 (Ollama app must be running)\n")

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user:
            continue
        if user.lower() in {"quit", "exit", "q"}:
            print("Bye.")
            break

        history.append({"role": "user", "content": user})
        try:
            reply = ollama.chat(model=MODEL, messages=history)
            text = reply["message"]["content"]
        except Exception as exc:
            print(
                f"AI error: {exc}\n"
                "Tips:\n"
                "  1) Open Ollama from Applications (menu-bar icon)\n"
                "  2) ollama list   # model must appear\n"
                f"  3) ollama pull {MODEL}\n"
            )
            history.pop()
            continue

        history.append({"role": "assistant", "content": text})
        print(f"AI: {text}\n")


if __name__ == "__main__":
    main()
