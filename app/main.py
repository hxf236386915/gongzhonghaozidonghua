from fastapi import FastAPI, status
from app.api.endpoints import articles

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(articles.router, prefix="/api/articles", tags=["articles"])