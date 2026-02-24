import os
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from langgraph.prebuilt import create_react_agent

from tools import query_amazon_reports, retrieve_realtime_stock_price, retrieve_historical_stock_price

load_dotenv()

tools = [query_amazon_reports, retrieve_realtime_stock_price, retrieve_historical_stock_price]

llm = ChatBedrockConverse(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name=os.getenv("AWS_REGION", "us-east-2"),
    max_tokens=4096
)
agent_app = create_react_agent(llm, tools)
try:
    from langfuse.decorators import observe
except (ImportError, ModuleNotFoundError):
    def observe(*args, **kwargs): return lambda f: f

SYSTEM_PROMPT = (
    "You are the Elite Amazon Financial Analyst Agent. "
    "CRITICAL TEMPORAL CONTEXT: Today is Monday, February 16, 2026. "
    "This means Q4 2024 and the entire year 2025 are now HISTORICAL DATA. "
    "\n\nPROTOCOL:\n"
    "1. For stock prices from 2024 or 2025, ALWAYS use 'retrieve_historical_stock_price'.\n"
    "2. For real-time quotes, use 'retrieve_realtime_stock_price'.\n"
    "3. For specific data about Amazon's business, office space, or AI strategy, "
    "query the 'Amazon Knowledge Base' tool.\n"
    "4. Be precise, data-driven, and professional. Always cite the specific tool or report used."
)

@observe()
async def run_agent_trace(message: str):
    """
    Ejecución del agente con inyección de Persona y Anclaje Temporal.
    """
    inputs = {
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("user", message)
        ]
    }
    return agent_app.astream(inputs, version="v2")