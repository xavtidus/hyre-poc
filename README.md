# Hyre AI PoC – Capability Assessment

**Candidate:** Xavier Hutchinson  
**Role:** Principal AI Engineer / Architect  
**Date:** 27 October 2025

---

## Objective
Demonstrate **end-to-end ownership** of:
- RAG pipeline (LlamaIndex + LlamaCloud + Pinecone)
- Agentic workflows (LangGraph ReAct with tool calling)
- Production-ready API (FastAPI)
- Secure, observable, and containerized design
- IaC foundation (Terraform-ready)

---

## Tech Stack (Current Implementation)
| Component       | Tool Used                    |
|----------------|------------------------------|
| LLM             | GPT-4o-mini                  |
| RAG             | LlamaIndex 0.11.16           |
| Document Parse  | LlamaCloud                   |
| Vector DB       | Pinecone + In-Memory (mock)  |
| Agents          | LangGraph 1.0.1 (ReAct)      |
| API             | FastAPI 0.115.0              |
| Tools           | DuckDuckGo Search            |
| Container       | Docker (production-ready)    |
| Orchestration   | Kubernetes (EKS planned)     |
| IaC             | Terraform (multi-cloud)      |
| Cloud           | AWS / GCP / Azure            |

---

## Project Structure
```
hyre-poc/
├── app/
│   ├── rag/                  # RAG pipeline + FastAPI
│   │   ├── api.py            # Main app: /ask, /agent, /test
│   │   └── rag_engine.py     # LlamaIndex + Pinecone/In-Memory
│   └── agents/               # LangGraph ReAct agent
│       ├── agent.py          # ReAct logic + tools
│       └── api.py            # /agent router
├── data/hyre_docs/           # Source documents
│   ├── hyre_job_pd.txt
│   ├── xavier_cv_summary.txt
│   └── docs/*.pdf            # Website pages
├── infra/                    # Terraform (AWS EKS + VPC)
├── docs/                     # Architecture + Loom script
├── .env.example              # Template (git-safe)
├── .gitignore                # Blocks .env
├── Dockerfile                # Production container
├── requirements.txt
└── README.md
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Docker
- OpenAI API key
- Pinecone API key (optional for local dev)

### Setup
```bash
git clone https://github.com/xavtidus/hyre-poc.git
cd hyre-poc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure secrets
cp .env.example .env
# Edit .env → add OPENAI_API_KEY, PINECONE_API_KEY
```

### Run Locally
```bash
uvicorn app.rag.api:app --reload --port 8000
# → http://localhost:8000/test
```

### Run in Docker (No Pinecone Key Needed)
```bash
docker build -t hyre-poc .
docker run -p 8000:8000 --env-file .env hyre-poc
# → MOCK_PINECONE=true → in-memory vector store
```

---

## API Endpoints

### Health
```bash
curl http://localhost:8000/
```

### RAG Query (`/ask`)
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the salary range?"}'
# → "$200k+"
```

### Agent Query (`/agent`)
```bash
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Compare Hyre job requirements with Xavier'\''s AWS experience"}'
# → ReAct reasoning + final answer
```

### Interactive Test
→ `http://localhost:8000/test`

---

## Implementation Status

### Completed
- RAG with **LlamaIndex + LlamaCloud parsing**
- **LangGraph ReAct agent** with `rag_search` + `web_search`
- **FastAPI** with streaming, validation, health
- **Docker** with **mock mode** (no Pinecone key needed)
- **Terraform** foundation (EKS, VPC, Secrets)
- **Git-safe secrets** (`.env.example`, `.gitignore`)
- **Architecture diagram** (Mermaid)

### Up Next
- Full **EKS deployment**
- **OpenTelemetry** tracing
- **CI/CD** with GitHub Actions
- **Loom demo** (3 mins)

---

## Agent Capabilities

- **Multi-step reasoning**
- **Tool selection** (internal vs. external)
- **Context-aware** responses
- **Verbose trace** in logs

---

## Security & Best Practices

- **Secrets**: `.env` (ignored), Docker `MOCK_PINECONE`
- **Validation**: Pydantic
- **Error handling**: 5xx with detail
- **Observability**: Logs + (planned) OpenTelemetry
- **Containerization**: Multi-stage Dockerfile

---

## Ethical AI Acknowledgement

This documentation was enhanced with AI assistance (GitHub Copilot) for clarity and structure.  
**All code, architecture, and implementation decisions are original work by Xavier Hutchinson.**

---

**GitHub:** [https://github.com/xavtidus/hyre-poc](https://github.com/xavtidus/hyre-poc)  
**Live Demo:** `docker run` or `uvicorn`  
**Architecture:** `docs/architecture.md` 