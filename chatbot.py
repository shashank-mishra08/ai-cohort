"""
Day 3 skeleton — local CLI chatbot (Ollama).

Usage:
  source .venv/bin/activate
  python3 chatbot.py

Type 'quit' to exit. Needs Ollama running locally with a model pulled
(e.g. `ollama pull llama3.2` or whatever model you use).
"""

from __future__ import annotations

import sys

try:
    import ollama
except ImportError:
    print("Install ollama package: pip install ollama")
    sys.exit(1)

# Change if you pulled a different model
MODEL = "llama3.2"


def main() -> None:
    history: list[dict[str, str]] = []
    print("Local coverage chatbot — type 'quit' to exit")
    print(f"Model: {MODEL} (Ollama must be running)\n")

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
        except Exception as exc:  # connection / missing model
            print(
                f"AI error: {exc}\n"
                "Tips: start Ollama app, then `ollama pull llama3.2`, retry."
            )
            history.pop()
            continue

        history.append({"role": "assistant", "content": text})
        print(f"AI: {text}\n")


if __name__ == "__main__":
    main()
