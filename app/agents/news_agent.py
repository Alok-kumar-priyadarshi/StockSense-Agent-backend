from app.tools.search_tool import search_news
from app.cache.cache import get_cache , set_cache


def get_news(company: str):

    cache_key = f"news:{company}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    query = f"{company} latest news stock market"
    results = search_news(query)

    news_list = [
        {
            "title": r.get("title"),
            "content": r.get("content"),
            "url": r.get("url")
        }
        for r in results
    ]

    set_cache(cache_key, news_list)

    return news_list