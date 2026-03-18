import time 
CACHE = {}

def get_cache(key:str):
    data = CACHE.get(key)
    if not data:
        return None
    
    # expire after 5 minutes
    if time.time() - data["timestamp"]>600:
        del CACHE[key]
        return None
    
    return data["value"]

def set_cache(key: str , value):
    CACHE[key] = {
        "value":value,
        "timestamp":time.time()
    } 