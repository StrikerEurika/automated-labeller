from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import annotate
import warnings

# Suppress known deprecation warnings from ML dependencies
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="transformers")
warnings.filterwarnings("ignore", category=UserWarning, module="torch")
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="groundingdino")

app = FastAPI(title="AutoAnnotate API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(annotate.router, prefix="/api/v1")
# app.include_router(batch.router, prefix="/api/v1")
