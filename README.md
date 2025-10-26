# Hyre AI PoC – Principal Architect Submission

**Candidate:** Xavier Hutchinson  
**Role:** Principal AI Engineer / Architect (Hyre, Sydney)  
**Date:** October 2025

---

## Objective
Demonstrate **end-to-end ownership** of:
- RAG pipeline (LlamaIndex + LLM Cloud)
- Agentic workflows (LangGraph ReAct)
- Multi-cloud infra (Terraform on AWS/GCP/Azure)
- Secure, observable, production-ready design

---

## Tech Stack (Current Implementation)
| Component       | Tool Used              |
|----------------|------------------------|
| LLM             | GPT-4o-mini            |
| RAG             | LlamaIndex 0.14.6      |
| Vector DB       | LlamaCloud + Pinecone  |
| Agents          | LangGraph 1.0.1        |
| API             | FastAPI 0.120.0        |
| Tools           | DuckDuckGo Search      |
| Container       | Docker (planned)       |
| Orchestration   | Kubernetes (planned)   |
| IaC             | Terraform (in progress) |
| Cloud           | AWS / GCP / Azure      |

---

## Project Structure
```
hyre-poc/
├── app/
│   ├── rag/              # RAG pipeline + FastAPI endpoints
│   │   ├── api.py        # Main FastAPI app with /ask, /agent, /test
│   │   └── rag_engine.py # LlamaIndex RAG implementation
│   └── agents/           # LangGraph ReAct agent with tools
│       ├── agent.py      # Agent with rag_search & web_search tools
│       └── api.py        # Agent FastAPI router
├── data/hyre_docs/       # Documents for RAG ingestion
│   ├── hyre_company_profile.txt
│   ├── hyre_job_pd.txt
│   ├── Xavier-Hutchinson-CV-OCT-2025-AU.pdf
│   └── *.pdf             # Website docs, testimonials
├── infra/                # Terraform modules (multi-cloud)
├── docs/                 # Architecture diagrams and design docs
├── agents/               # Legacy agent code (deprecated)
├── .env                  # Local secrets (gitignored)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## Quick Start

### Prerequisites
- Python 3.13+
- OpenAI API key
- LlamaCloud API key (for document parsing)

### Setup
```bash
# 1. Clone and activate
git clone https://github.com/xavtidus/hyre-poc.git
cd hyre-poc
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# OPENAI_API_KEY=your_openai_key
# LLAMA_CLOUD_API_KEY=your_llamacloud_key
```

### Run the Application
```bash
# Start the FastAPI server
uvicorn app.rag.api:app --reload --port 8000

# Server will be available at http://localhost:8000
# Interactive test page: http://localhost:8000/test
```

---

## API Endpoints & Sample Queries

### 1. Health Check
```bash
curl http://localhost:8000/
```

### 2. RAG Query (`/ask`) - Direct document search
```bash
# About Hyre company
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Hyre's company mission and focus areas?"}'

# Office location
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Where is Hyre located and what is their contact information?"}'

# Job requirements
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the key technical requirements for the Principal AI Engineer role?"}'

# Candidate background
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Xavier Hutchinson's experience with AWS and cloud technologies?"}'
```

### 3. Agent Query (`/agent`) - ReAct agent with tools
The agent can use both internal RAG search and web search to answer questions.

```bash
# Compare job requirements with candidate skills
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Compare Hyre job requirements with Xavier'\''s AWS experience"}'

# Market research with web search
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the latest trends in AI consulting in Australia?"}'

# Technical architecture question
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"question": "How should I design a RAG pipeline for financial services compliance?"}'

# Company and role analysis
curl -X POST http://localhost:8000/agent \
  -H "Content-Type: application/json" \
  -d '{"question": "Based on Hyre's company profile, what specific AI solutions could help their recruitment process?"}'
```

---

## Implementation Status

### ✅ Completed
- **RAG Pipeline**: LlamaIndex with LlamaCloud document parsing
- **Vector Storage**: Configured for Pinecone and LlamaCloud
- **FastAPI Backend**: RESTful API with streaming responses
- **Agent Framework**: LangGraph ReAct agent with tool calling
- **Tools Integration**: 
  - `rag_search`: Query internal Hyre documents and CV
  - `web_search`: DuckDuckGo web search for external information
- **Document Ingestion**: Automated processing of PDF and text files
- **Interactive Testing**: Web-based test interface at `/test`

### 🔄 Up Next
- **Infrastructure as Code**: Terraform modules for multi-cloud deployment
- **System Architecture**: Security, observability, and scalability design
- **Containerization**: Docker configuration for production deployment
- **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

### 📋 Planned
- **Kubernetes Deployment**: Production-ready orchestration
- **Multi-cloud Strategy**: AWS EKS, GCP GKE, Azure AKS configurations
- **Monitoring & Observability**: OpenTelemetry integration
- **Security Hardening**: IAM, secrets management, network policies

---

## Agent Capabilities

The LangGraph ReAct agent (`/agent` endpoint) provides:

- **Reasoning**: Step-by-step thought process for complex queries
- **Tool Selection**: Intelligent choice between internal RAG and web search
- **Multi-step Planning**: Breaks down complex questions into sub-queries
- **Context Awareness**: Maintains conversation context and state

**Available Tools:**
- `rag_search`: Searches Hyre company docs, job descriptions, and candidate CV
- `web_search`: Public web search for current information and trends

---

## Data Sources

The RAG system is trained on:
- **Hyre Company Profile**: Mission, services, team size, contact info
- **Job Description**: Principal AI Engineer role requirements and tech stack  
- **Candidate CV**: Xavier Hutchinson's experience and qualifications
- **Website Content**: Achievements, testimonials, and additional company info

---

## Security & Best Practices

- **API Key Management**: Environment-based configuration
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: Comprehensive exception handling and logging
- **Rate Limiting**: (Planned) Request throttling for production use
- **Secrets Management**: (Planned) AWS Secrets Manager / GCP Secret Manager integration

---

## Ethical AI Acknowledgement

This documentation was created with AI assistance (GitHub Copilot) to enhance clarity, structure, and completeness. All source code, architectural decisions, and technical implementations are original human work by Xavier Hutchinson. AI was used solely for documentation generation, formatting, and content organization from existing human-authored code and technical artifacts.

The core technical contributions—including the RAG pipeline design, LangGraph agent implementation, API architecture, and infrastructure planning—represent original engineering work and domain expertise.

---

**GitHub Repository:** [https://github.com/xavtidus/hyre-poc](https://github.com/xavtidus/hyre-poc)  
**Live Demo:** Available on request  
**Architecture Documentation:** See `docs/` directory