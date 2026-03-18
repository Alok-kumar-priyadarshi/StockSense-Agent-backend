from app.services.ticker_service import resolve_company_to_ticker
from app.tools.finance_tool import get_stock_data_by_ticker
from app.cache.cache import get_cache, set_cache


def get_finance_data(company: str):

    cache_key = f"finance:{company}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    ticker = resolve_company_to_ticker(company)

    if not ticker:
        return {"error": "Ticker not found"}

    data = get_stock_data_by_ticker(ticker)

    result = {
        "ticker": ticker,
        "data": data
    }

    set_cache(cache_key, result)

    return result