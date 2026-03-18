from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Financial Intelligence API")

app.include_router(router)