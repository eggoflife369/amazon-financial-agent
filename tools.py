import os
import yfinance as yf
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from langchain_core.tools import tool

@tool
def query_amazon_reports(query: str):
    """Retrieves financial data and narrative insights from Amazon's official annual and quarterly reports."""
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id=os.getenv("KNOWLEDGE_BASE_ID"),
        region_name=os.getenv("AWS_REGION", "us-east-2"),
        retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 15}}
    )
    docs = retriever.invoke(query)
    return "\n\n".join([d.page_content for d in docs]) if docs else "No relevant data found in the reports."

@tool
def retrieve_realtime_stock_price(symbol: str = "AMZN"):
    """Fetches the most recent closing stock price for a given ticker symbol."""
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="1d")
    return f"Latest Price for {symbol}: ${df['Close'].iloc[-1]:.2f}" if not df.empty else "Error: Could not fetch real-time data."

@tool
def retrieve_historical_stock_price(symbol: str, start_date: str, end_date: str):
    """
    Fetches historical closing prices for a stock. 
    Dates must be in 'YYYY-MM-DD' format.
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(start=start_date, end=end_date)
    if hist.empty:
        return "No historical data found for the specified range."
    return str(hist['Close'].to_dict())