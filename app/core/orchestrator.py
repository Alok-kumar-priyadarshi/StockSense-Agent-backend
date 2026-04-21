from app.agents.news_agent import get_news
from app.agents.finance_agent import get_finance_data
from app.agents.reasoning_agent import analyze_impact
from app.core.router import route_query
from app.core.guardrails import apply_guardrails
from app.utils.logger import log_info, log_error
from app.memory.memory_store import get_memory, update_memory
from app.utils.validators import is_valid_company_name, validate_company_llm

def run_pipeline(query: str, user_id: str = "default"):

    memory = get_memory(user_id)

    routing = route_query(query)

    intent = routing.get("intent")
    companies = routing.get("companies", [])

    # 🧠 MEMORY FIX
    if (
        not companies
        and intent in ["IMPACT_ANALYSIS", "WHY_MOVEMENT"]
        and memory.get("last_company")
    ):
        companies = [memory["last_company"]]

    valid_companies = []

    for c in companies:

        # ✅ First: fast rule check
        if is_valid_company_name(c):
            valid_companies.append(c)
            

        # ✅ Second: LLM validation (fallback)
        elif validate_company_llm(c):
            valid_companies.append(c)

    # ❌ If nothing valid → reject
    if not valid_companies:
        return {
            "message": "Please enter a valid company name (e.g., Tesla, Apple)"
        }

    companies = valid_companies

    results = []

    for company in companies:

        news_data = get_news(company)
        finance_data = get_finance_data(company)

        analysis = analyze_impact(company, news_data, finance_data)

        guarded = apply_guardrails(analysis)
        if "error" in guarded:
            return guarded

        result = {
            "company": company,
            "event_summary": [n["title"] for n in news_data],
            **guarded
        }

        results.append(result)

        # 🧠 update memory
        update_memory(user_id, {
            "last_company": company,
            "last_query": query
        })

    return results