from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import rag

app = FastAPI(
    title="StudyMate AI - Advanced Backend",
    description="Production-grade API for Retrieval-Augmented Generation.",
    version="1.0.0"
)

# Enable CORS for the Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rag.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy"}
