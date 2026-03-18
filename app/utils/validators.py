import re
from app.llm.provider import get_llm_response


def validate_router_output(data:dict):
    
    required_keys = ["intent" , "companies" , "time_range" , "requires_clarification"]
    
    for key in required_keys:
        if key not in data:
            return False
        
    if not isinstance(data["companies"],list):
        return False
    
    return True

def is_valid_company_name(name: str):

    # ❌ reject random strings (no vowels / too random)
    if len(name) < 1:
        return False

    # must contain at least one vowel
    if not re.search(r"[aeiouAEIOU]", name):
        return False

    # reject long random strings
    if len(name) > 15:
        return False

    return True

def validate_company_llm(name: str) -> bool:

    prompt = f"""
    Determine if "{name}" is a real, well-known company.

    Rules:
    - Answer ONLY YES or NO
    - If unsure → answer NO
    - Random strings → NO
    - Must be a recognized business entity

    Examples:
    Tesla → YES
    Apple → YES
    nfjvnkfdbvkfbvjknbffg → NO
    xyzrandom → NO
    """

    try:
        response = get_llm_response(prompt)
        print("VALIDATION LLM:", name, "→", response)

        return response.strip().lower() == "yes"

    except:
        return False

