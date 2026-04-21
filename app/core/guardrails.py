import re

def apply_guardrails(response: dict):

    text = str(response).lower()

    forbidden = [r"\bbuy\b", r"\bsell\b", r"\binvest\b", r"\bguaranteed\b", r"\bpurchase\b", r"\brecommend\b", r"\bportfolio\b"]
    forbidden2 = [r"\bbomb\b", r"\bguns\b", r"\bdrugs\b", r"\btrafficking\b", r"\bfuck\b"]

    for pattern in forbidden:
        if re.search(pattern, text):
            return {
                "error": "This system does not provide financial advice"
            }

    for pattern in forbidden2:
        if re.search(pattern, text):
            return {
                "error": "This system does not accept queries with that content"
            }

    if "confidence" not in response:
        response["confidence"] = "low"

    return response
