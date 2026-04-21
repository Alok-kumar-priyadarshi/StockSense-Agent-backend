import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

BACKEND_URL = os.getenv("BACKEND_URL")
if not BACKEND_URL:
    BACKEND_URL = "http://localhost:8000/analyze"
