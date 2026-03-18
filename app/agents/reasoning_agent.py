from app.llm.provider import get_llm_response
from app.llm.prompts import REASONING_PROMPT
from app.llm.parser import parse_llm_output

def add_conclusion(parsed):

    impact = parsed.get("impact_direction", "").lower()

    if "positive" in impact or "bullish" in impact:
        conclusion = "Stock may increase"
    elif "negative" in impact or "bearish" in impact:
        conclusion = "Stock may decrease"
    else:
        conclusion = "Stock may remain stable"

    parsed["conclusion"] = conclusion

    parsed["disclaimer"] = (
        "This is an AI-generated analysis based on available data. "
        "It is not financial advice and may be incorrect "
        "So never trust or make any decision with this conclusion."
    )

    return parsed



def analyze_impact(company , news , finance):
    prompt = REASONING_PROMPT.format(
        company=company,
        news=news,
        finance=finance
    )
    
    raw_response = get_llm_response(prompt)
    parsed = parse_llm_output(raw_response)
    
    parsed = add_conclusion(parsed)
    
    if not parsed.get("reasoning_chain"):
        parsed["reasoning_chain"] = ["Insufficient reasoning"]

    return parsed



