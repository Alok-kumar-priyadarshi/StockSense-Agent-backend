def apply_guardrails(response: dict):

    text = str(response).lower()

    forbidden = ["buy", "sell", "invest", "guaranteed" , "purchase" , "recommend" ]

    if any(word in text for word in forbidden):
        return {
            "error": "This system does not provide financial advice"
        }

    # ensure confidence exists
    if "confidence" not in response:
        response["confidence"] = "low"

    return response