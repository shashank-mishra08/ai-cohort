# Day 2 + Day 3 status (this machine)

Project path: `/Users/shashank/projects/my-first-app`  
GitHub: `https://github.com/shashank-mishra08/ai-cohort`

---

## Day 2 — Ollama + AI coding assistant

| Step | Status |
|------|--------|
| Install Ollama | ✅ App + CLI |
| `ollama --version` | ✅ 0.32.0 |
| Pull model for **8 GB RAM** | ✅ `qwen2.5-coder:3b` (use 3b, not 7b) |
| Test `ollama run …` | ✅ works |
| API `http://localhost:11434` | ✅ “Ollama is running” |
| Cline extension | ✅ installed (`saoudrizwan.claude-dev`) |
| Copilot Chat | ✅ available in VS Code |
| Select Ollama model in UI | ⬜ do once in VS Code (Cline or Copilot Manage Models) |

**Verify anytime:**

```bash
curl http://localhost:11434
ollama list
cd /Users/shashank/projects/my-first-app
python3 day02_verify_ollama.py
```

**Wire Cline (easiest on this Mac):**

1. Open Cline panel in VS Code  
2. API Provider = Ollama  
3. Base URL = `http://localhost:11434`  
4. Model = `qwen2.5-coder:3b`  
5. Prompt: `write a python function that checks if a number is prime`

---

## Day 3 — First project pieces

| Deliverable | Status | Where |
|-------------|--------|--------|
| Project folder | ✅ | `my-first-app` |
| CLI chatbot vs local model | ✅ | `chatbot.py` (model `qwen2.5-coder:3b`) |
| FastAPI backend `/health` | ✅ | `coverage-chatbot-api/` |
| React frontend scaffold | ✅ | `coverage-chatbot-web/` (Vite + React) |
| Git + GitHub remote | ✅ | `origin` → `ai-cohort` |

### Run CLI chatbot

```bash
# Ollama app must be running
cd /Users/shashank/projects/my-first-app
source .venv/bin/activate
python3 chatbot.py
# try: write a python function to reverse a string
# then: quit
```

### Run API health

```bash
cd /Users/shashank/projects/my-first-app
source .venv/bin/activate
cd coverage-chatbot-api
uvicorn app:app --reload --port 8000
# browser: http://localhost:8000/health  → {"status":"ok"}
```

### Run React scaffold

```bash
cd /Users/shashank/projects/my-first-app/coverage-chatbot-web
npm install
npm run dev
# open the URL Vite prints (usually http://localhost:5173)
```

### Git workflow you use every day

```bash
cd /Users/shashank/projects/my-first-app
git status
git add .
git commit -m "Describe your change"
git push origin main
```

---

## Note on “Day 2 vs Day 3” text

Course text sometimes mixes:

- **Day 2 focus:** install Ollama + connect VS Code (Copilot/Cline)  
- **Day 3 focus:** chatbot.py + backend + React + git  

On this Mac, **both cores are ready**. Only remaining “click once” step is selecting Ollama inside Cline/Copilot Chat.
