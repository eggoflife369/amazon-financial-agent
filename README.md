Amazon Financial AI Agent: Enterprise Edition
An industrial-grade, containerized AI solution designed for real-time financial analysis and high-precision data extraction from Amazon (AMZN) SEC Filings. Built with the cutting-edge AWS Generative AI stack, LangGraph, and a Zero-Trust security model.

Engineering Architecture
The system operates on a decoupled, modular architecture separating the API routing, cognitive reasoning, and external integrations.

Stateful Orchestration: A ReAct Agent developed in LangGraph, managing dynamic reasoning across multiple tools.

Temporal Grounding (2026 Sync): The system operates with strict real-time awareness (Current date: February 16, 2026). This allows precise historical analysis of 2024 and 2025 data, bypassing LLM training data cut-offs.

High-Precision RAG: Native integration with Amazon Bedrock Knowledge Bases to query annual reports (10-K) and earnings releases with metadata filtering.

Financial Tooling: Direct connection to the Yahoo Finance API for live market data and historical price trends.

Technology Stack
Orchestrator: LangGraph (Stateful Agentic workflows)

Model: Claude 3.5 Sonnet (Reasoning & Tool Use via Bedrock)

Backend: FastAPI (High-performance Python API Controller)

Frontend: Streamlit (Reactive User Interface)

Containerization: Docker (Environment isolation & cloud deployment readiness)

Security: AWS Cognito & IAM (Identity Management, JWT Auth & Zero-Trust Policies)

Observability: Langfuse (V3 Tracing, Prompt Mgmt & Cost Analysis)

Infrastructure: Terraform (IaC provisioning for Cognito, S3, IAM Roles)

Deployment Guide
1. Infrastructure as Code (IaC)
Deploy the required AWS security, storage, and identity services automatically. This includes the S3 bucket for financial reports, Cognito User Pools, and the execution IAM Roles required for Amazon Bedrock:

terraform init
terraform apply
> Note: Upon completion, Terraform will output the client_id, client_secret, and s3_bucket_name required for your .env file.

2. Environment Configuration (.env)
Create a .env file based on the provided .env.example:

AWS_REGION=us-east-2
USER_POOL_ID=us-east-2_XXXXX
CLIENT_ID=XXXXX
COGNITO_CLIENT_SECRET=XXXXX
KNOWLEDGE_BASE_ID=XXXXX
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST="https://cloud.langfuse.com"
3. Application Execution (Two Options)
Option A: Containerized (Production Standard)
Build and run the backend using Docker:

docker build -t amazon-financial-agent .
docker run -p 8000:8000 --env-file .env amazon-financial-agent
Option B: Local Virtual Environment

python -m venv venv
# Windows: .\venv\Scripts\activate | Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
Terminal 1 (Backend): python main.py

Terminal 2 (Frontend): streamlit run app.py

Evaluation Protocol (User Acceptance Criteria)
To validate the system's full capabilities against the project requirements, execute the following exact queries in the Streamlit UI or the provided demo.ipynb notebook:

Market Real-time: "What is the stock price for Amazon right now?"

Temporal Logic: "What were the stock prices for Amazon in Q4 last year?"

Deep RAG Retrieval: "What is the total amount of office space Amazon owned in North America in 2024?"

Analyst Comparison: "Compare Amazon's recent stock performance to what analysts predicted in their reports"

Business Strategy: "I'm researching AMZN give me the current price and any relevant information about their AI business"

Security & Observability
Authentication: The /chat endpoint is protected. It requires a valid Bearer Token generated via AWS Cognito.

Zero-Trust IAM: The backend operates under a strict IAM role containing only AmazonBedrockFullAccess, adhering to least-privilege principles.

Observability: Every reasoning step (Thought, Tool Call, Output) is logged in Langfuse Cloud. This provides a full audit trail and real-time cost monitoring.


## Project Demos
* [**UI & Authentication Flow**](https://youtu.be/KUWZYsZH7Do) - Full demo of the Streamlit interface and AWS Cognito login.
* [**Backend & Notebook Trace**](https://youtu.be/v96GMhtlAgA) - Detailed execution of the LangGraph agent and Langfuse traces.



Note for the Reviewer



This project implements a Temporal Bias Bypass within the System Prompt. This ensures the LLM treats 2024 and 2025 data as historical facts rather than future predictions, overcoming standard model knowledge limitations.



