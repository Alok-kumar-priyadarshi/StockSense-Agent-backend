
from app.llm.provider import get_llm_response
from app.llm.prompts import ROUTER_PROMPT
from app.llm.parser import parse_llm_output
from app.utils.retry import retry

from app.utils.validators import validate_router_output


def llm_route(query: str):

    def call():
        prompt = ROUTER_PROMPT.format(query=query)
        return get_llm_response(prompt)

    raw = retry(call, retries=2)

    parsed = parse_llm_output(raw)

    return parsed

def fallback_company_extraction(query: str):

    words = query.lower().split()

    # pick meaningful words (ignore stop words)
    ignore = {"what", "is", "the", "about", "your", "though", "think","tell","me"}

    candidates = [w for w in words if w not in ignore]

    if candidates:
        return [candidates[-1].capitalize()]  # last meaningful word

    return []

def extract_company_llm(query: str):

    prompt = f"""
    Extract company names from the query.

    Return ONLY a JSON list of company names.

    Query: {query}
    """

    response = get_llm_response(prompt)

    parsed = parse_llm_output(response)

    if isinstance(parsed, list):
        return parsed
    
    print("LLM EXTRACT:", parsed)

    return []


def route_query(query: str):

    try:
        result = llm_route(query)

        # 🔥 NEW: LLM-based company extraction
        companies = extract_company_llm(query)

        # fallback if LLM fails
        if not companies:
            companies = fallback_company_extraction(query)

        result["companies"] = companies

        if not validate_router_output(result):
            raise Exception("Invalid router output")

        return result

    except Exception:
        fallback = fallback_company_extraction(query)

        return {
            "intent": "GENERAL",
            "companies": fallback,
            "time_range": "24h",
            "requires_clarification": False if fallback else True,
        }

