import json
import re

def extract_json(text: str):
    try:
        match = re.search(r"\[.*\]|\{.*\}", text, re.DOTALL)
        if match:
            return match.group()
        return None
    except:
        return None


def parse_llm_output(response: str):

    try:
        parsed = json.loads(response)

        # ✅ allow list OR dict
        if isinstance(parsed, (list, dict)):
            return parsed

    except:
        pass

    json_str = extract_json(response)

    if json_str:
        try:
            parsed = json.loads(json_str)

            if isinstance(parsed, (list, dict)):
                return parsed
        except:
            pass

    return []