import yfinance as yf

def get_stock_data(company:str):
    """
    Try to feetch stock data dynamically.
    """
    
    try:
        ticker = yf.Ticker(company)
        info = ticker.info
        
        return {
            "longName":info.get("longName"),
            "sector": info.get("sector"),
            "industry":info.get("industry"),
            "marketCap":info.get("marketCap")
        }
        
    except Exception:
        return {}

def get_stock_data_by_ticker(ticker: str):

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "symbol": ticker,
            "longName": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "marketCap": info.get("marketCap")
        }

    except Exception:
        return {}


