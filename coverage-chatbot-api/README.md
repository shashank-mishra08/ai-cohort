# coverage-chatbot-api

FastAPI skeleton for the healthcare coverage chatbot program (Day 3+).

## Setup

```bash
# from repo root
source .venv/bin/activate
pip install -r coverage-chatbot-api/requirements.txt
```

## Run

```bash
cd coverage-chatbot-api
uvicorn app:app --reload --port 8000
```

Open:
- Health: http://localhost:8000/health → `{"status":"ok"}`
- Docs: http://localhost:8000/docs

Later days extend this API with `/chat`, retrieval, tools, and streaming.
