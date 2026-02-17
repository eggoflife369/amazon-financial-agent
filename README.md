📈 Amazon Financial AI Agent: Enterprise Edition



An industrial-grade AI solution designed for real-time financial analysis and high-precision data extraction from Amazon (AMZN) SEC Filings. Built with the cutting-edge AWS Generative AI stack and LangGraph.



🧠 Engineering Architecture



The system's core is a ReAct Agent developed in LangGraph, orchestrating dynamic reasoning across multiple sources of truth:



Temporal Grounding (2026 Sync): The agent operates with real-time awareness (Current date: February 16, 2026). This allows precise historical analysis of 2024 and 2025 data, bypassing LLM training data cut-offs.



High-Precision RAG: Native integration with Amazon Bedrock Knowledge Bases to query annual reports (10-K) and earnings releases with metadata filtering.



Financial Tooling: Direct connection to the Yahoo Finance API for live market data and historical price trends.



🛠️ Technology Stack



Component



Technology



Role



Orchestrator



LangGraph



Stateful Agentic workflows



Model



Claude 3.5 Sonnet



Reasoning \& Tool Use (via Bedrock)



Backend



FastAPI



High-performance Python API



Frontend



Streamlit



Reactive User Interface



Security



AWS Cognito



Identity Management \& JWT Auth



Observability



Langfuse



V3 Tracing, Prompt Mgmt \& Cost Analysis



Infrastructure



Terraform



Infrastructure as Code (IaC)



🚀 Deployment Guide



1\. Environment Preparation (VENV)



Operating within a virtual environment ensures version compatibility and dependency isolation.



\# Create and activate the environment (Windows)

python -m venv venv

.\\venv\\Scripts\\activate



\# Install dependencies

pip install -r requirements.txt





2\. Infrastructure as Code (IaC)



Deploy the required AWS security and identity services automatically:



terraform init

terraform apply





Note: Upon completion, Terraform will output the client\_id and client\_secret required for your .env file.



3\. Environment Configuration (.env)



Create a .env file based on the provided .env.example.



AWS\_REGION=us-east-2

USER\_POOL\_ID=us-east-2\_XXXXX

CLIENT\_ID=XXXXX

COGNITO\_CLIENT\_SECRET=XXXXX

KNOWLEDGE\_BASE\_ID=XXXXX

LANGFUSE\_PUBLIC\_KEY=pk-lf-...

LANGFUSE\_SECRET\_KEY=sk-lf-...

LANGFUSE\_HOST="\[https://cloud.langfuse.com](https://cloud.langfuse.com)"





4\. Running the System



You need two active terminals with the venv activated:



Terminal 1 (Backend): python main.py



Terminal 2 (Frontend): streamlit run app.py



🎯 Evaluation Protocol (User Acceptance Criteria)



To validate the system's full capabilities, execute the following queries in the Streamlit UI or the provided demo.ipynb:



Market Real-time: "What is the stock price for Amazon right now?"



Temporal Logic: "What were the stock prices for Amazon in Q4 2024?"



Deep RAG Retrieval: "How much office space did Amazon own in North America in 2024?"



Analyst Comparison: "Compare recent performance vs analyst predictions in the reports."



Business Strategy: "Analyze AI business growth and AWS capacity from the latest releases."



🛡️ Security \& Observability



Authentication: The /chat endpoint is protected. It requires a valid Bearer Token generated via AWS Cognito.



Observability: Every reasoning step (Thought, Tool Call, Output) is logged in Langfuse Cloud. This provides a full audit trail and real-time cost monitoring.


## 📺 Project Demos
* [**UI & Authentication Flow**](https://youtu.be/KUWZYsZH7Do) - Full demo of the Streamlit interface and AWS Cognito login.
* [**Backend & Notebook Trace**](https://youtu.be/v96GMhtlAgA) - Detailed execution of the LangGraph agent and Langfuse traces.



💡 Note for the Reviewer



This project implements a Temporal Bias Bypass within the System Prompt. This ensures the LLM treats 2024 and 2025 data as historical facts rather than future predictions, overcoming standard model knowledge limitations.


