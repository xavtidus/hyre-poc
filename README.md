# Hyre AI PoC – Principal Architect Submission

**Candidate:** Xavier Hutchinson  
**Role:** Principal AI Engineer / Architect (Hyre, Sydney)  
**Date:** October 2025

---

## Objective
Demonstrate **end-to-end ownership** of:
- RAG pipeline (LlamaIndex + Pinecone)
- Agentic workflows (LangChain ReAct)
- Multi-cloud infra (Terraform on AWS/GCP/Azure)
- Secure, observable, production-ready design

---

## Tech Stack (as per PD)
| Component       | Tool Used              |
|----------------|------------------------|
| LLM             | GPT-4o / Claude 3      |
| RAG             | LlamaIndex             |
| Vector DB       | Pinecone + Weaviate    |
| Agents          | LangChain ReAct        |
| API             | FastAPI                |
| Container       | Docker                 |
| Orchestration   | Kubernetes (Minikube)  |
| IaC             | Terraform              |
| Cloud           | AWS / GCP / Azure      |

---

## Project Structure
```
hyre-poc/
├── app/
│   ├── rag/          # RAG pipeline + FastAPI endpoints
│   └── agents/       # ReAct agent with custom tools
├── infra/            # Terraform modules (multi-cloud)
├── data/hyre_docs/   # Sample documents for RAG ingestion
├── docs/             # Architecture diagrams and design docs
├── .env              # Local secrets (gitignored)
├── .gitignore
└── README.md
```

---

## Quick Start
```bash
# 1. Clone and activate
git clone git@github.com:yourname/hyre-poc.git
cd hyre-poc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (create this on Day 1)

# 2. Load secrets
cp .env.example .env  # Fill in API keys

# 3. Run RAG API (Day 1)
uvicorn app.rag.api:app --reload --port 8000

# 4. Test
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Hyre's AI strategy?"}'
```

---

## Deliverables by Day

### Day 1: Production-Ready RAG Pipeline
- Ingest docs → embed → store in Pinecone
- Query via FastAPI `/ask` endpoint
- Fully Dockerized

### Day 2: Agentic Workflow with ReAct
- Agent routes between internal RAG, web search, and code execution
- Reasoning trace output
- Tools: `rag_search`, `web_search`

### Day 3: Full Architecture + Deployment
- System design doc with security, observability, scalability
- Terraform: spins up EKS cluster + Vertex AI endpoint
- 3-minute Loom demo (code → API → agent → infra)

---

## Security & Best Practices (Embedded)
- **IAM**: Least privilege via Terraform
- **Secrets**: AWS Secrets Manager / GCP Secret Manager
- **Networking**: VPC endpoints, private subnets
- **Observability**: OpenTelemetry → CloudWatch / Prometheus
- **CI/CD**: GitHub Actions → Terraform → ArgoCD

---

**GitHub Repository:** [https://github.com/yourname/hyre-poc](https://github.com/yourname/hyre-poc)  
**Demo Video:** [loom.com/hyre-poc-demo](https://www.loom.com) *(recorded on Day 3)*