from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import articles, auth

app = FastAPI()

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])