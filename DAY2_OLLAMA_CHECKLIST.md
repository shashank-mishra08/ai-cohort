# Day 2 — Ollama + VS Code AI assistant checklist

## Your machine (verified)

| Check | Status | Notes |
|--------|--------|--------|
| Ollama installed | ✅ | `/Applications/Ollama.app` + `ollama` CLI |
| Local API | ✅ | `http://localhost:11434` → “Ollama is running” |
| Coding model pulled | ✅ | `qwen2.5-coder:3b` (~1.9 GB) |
| RAM guidance | ✅ | **8 GB RAM** → course says use **3b** (not 7b) |
| Model chat test | ✅ | `ollama run qwen2.5-coder:3b` returns code |
| Cline extension | ✅ | `saoudrizwan.claude-dev` installed in VS Code |
| GitHub Copilot Chat | ✅ | Built into VS Code (Copilot Chat) |
| Wire model into chat UI | ⬜ manual | Pick Ollama model in Copilot **or** Cline settings |

You do **not** need `qwen2.5-coder:7b` on 8 GB RAM. 3b is the correct course choice.

---

## Quick re-verify anytime

```bash
# 1) Ollama app open (menu bar icon)
ollama --version
ollama list
curl http://localhost:11434
# expect: Ollama is running

# 2) Chat test
ollama run qwen2.5-coder:3b
# type: write a python function to reverse a string
# type: /bye

# 3) Automated check
cd /Users/shashank/projects/my-first-app
python3 day02_verify_ollama.py
```

---

## Finish VS Code wiring (if chat still uses cloud only)

### Option A — GitHub Copilot Free (needs GitHub login)

1. Extensions (`Cmd+Shift+X`) → **GitHub Copilot** → Install (if needed) → Sign in  
2. Open Chat (`Cmd+Ctrl+I` or chat icon)  
3. Model dropdown under input → **Manage Models…**  
4. Select **Ollama** (Ollama app must be running)  
5. Check **`qwen2.5-coder:3b`** → OK  
6. Select that model in the dropdown  
7. Prompt: `write a python function that checks if a number is prime`  
8. Optional: turn Wi‑Fi off — should still answer  

### Option B — Cline (already installed, no GitHub required)

1. Extensions → **Cline** (publisher saoudrizwan) already installed  
2. Open Cline panel  
3. Settings:  
   - API Provider: **Ollama**  
   - Base URL: `http://localhost:11434`  
   - Model: **qwen2.5-coder:3b**  
4. Same prime-number prompt  
5. Offline test optional  

For the rest of the course, “Ask Copilot” = use **Cline** or **Copilot Chat** with Ollama selected.

---

## Deliverable

- [x] Ollama installed  
- [x] Coding model pulled and tested locally  
- [x] API on `http://localhost:11434`  
- [ ] VS Code chat confirmed using that local model (do Option A or B once in the UI)  
- [ ] Offline confirmation (optional but recommended)  

---

## Do not

- Don’t force `qwen2.5-coder:7b` on 8 GB — may hang or crash  
- Don’t commit API keys  
- Don’t need a separate “start server” if the Ollama app is running  
