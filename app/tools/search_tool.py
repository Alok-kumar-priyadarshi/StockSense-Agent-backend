import os
from tavily import TavilyClient
from dotenv import load_dotenv
from app.utils.retry import retry

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_news(query:str):
    def call():
        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )
        return response.get("results", [])

    return retry(call, retries=3, delay=2)
