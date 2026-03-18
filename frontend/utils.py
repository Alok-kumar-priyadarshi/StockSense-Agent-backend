import requests
from config import BACKEND_URL

def call_backend(query , user_id):
    try:
        response = requests.post(
            BACKEND_URL,
            json={
                "query":query,
                "user_id":user_id
            },
            timeout=20
        )
        
        return response.json()
    except Exception as e:
        return {
            "error":"Backend not reachable",
            "details":str(e)
        }
