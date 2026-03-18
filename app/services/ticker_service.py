import yfinance as yf
from app.tools.search_tool import search_news

def resolve_ticker(company:str):
    """
        Multi-step resolution:
    1. Try direct ticker
    2. Try search
    3. Fallback
    """
    
    
    
    # step 1 Try direct ticker
    try:
        stock = yf.Ticker(company)
        info = stock.info
        
        if info and info.get("symbol"):
            return info.get("symbol")
    except:
        pass
    
    # step2 try search via yfiance
    try:
        search = yf.Tickers(company)

        for ticker in search.tickers:
            return ticker # first match
    except:
        pass
    
    return None

def resolve_ticker_with_search(company: str):
    """
    Use Tavily to infer ticker symbol
    """

    query = f"{company} stock ticker symbol"

    results = search_news(query)

    for r in results:
        content = r.get("content", "")

        # simple heuristic: find uppercase ticker
        words = content.split()

        for w in words:
            if w.isupper() and 2 <= len(w) <= 5:
                return w

    return None


def resolve_company_to_ticker(company: str):

    # Step 1: direct
    ticker = resolve_ticker(company)
    if ticker:
        return ticker

    # Step 2: Tavily-based inference
    ticker = resolve_ticker_with_search(company)
    if ticker:
        return ticker

    return None



