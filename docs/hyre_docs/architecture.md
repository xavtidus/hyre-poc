# Hyre AI Platform — PoC

```mermaid
flowchart TD
    A[User / API] --> B[FastAPI Gateway]
    B --> C[RAG Engine<br>LlamaIndex + Pinecone]
    B --> D[ReAct Agent<br>LangChain + Tools]
    C --> E[Pinecone Vector DB]
    D --> E
    D --> F[DuckDuckGo Web Search]
    C --> G[OpenAI Embeddings]
    D --> H[OpenAI GPT-4o-mini]
    B --> I[AWS EKS Cluster]
    I --> J[Terraform IaC]
    I --> K[IAM Roles + Secrets Manager]
    I --> L[CloudWatch + OpenTelemetry]
```

## Security & Observability
- **IAM**: Least privilege via Terraform
- **Secrets**: AWS Secrets Manager
- **Networking**: VPC + private subnets
- **Observability**: OpenTelemetry → CloudWatch
- **CI/CD**: GitHub Actions → Terraform → ArgoCD

## Tech Stack (PD Match)
| Layer       | Tool Used              |
|-------------|------------------------|
| LLM         | GPT-4o / Claude 3      |
| RAG         | LlamaIndex             |
| Vector DB   | Pinecone               |
| Agents      | LangChain ReAct        |
| API         | FastAPI                |
| Container   | Docker                 |
| Orchestration | Kubernetes (EKS)     |
| IaC         | Terraform              |
| Cloud       | AWS (multi-cloud ready)|