def apply_guardrails(response: dict):

    text = str(response).lower()

    forbidden = ["buy", "sell", "invest", "guaranteed" , "purchase" , "recommend" , "portfolio"  ]
    forbidden2 = ["bomb","guns","drugs","Trafficking","fuck"] 
    

    if any(word in text for word in forbidden):
        return {
            "error": "This system does not provide financial advice"
        }
    if any(word in text for word in forbidden2):
        return {
            "error": "This system does not accept critical object names"
        }

    # ensure confidence exists
    if "confidence" not in response:
        response["confidence"] = "low"

    return response
