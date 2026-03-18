from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    query:str
    user_id: str | None = None