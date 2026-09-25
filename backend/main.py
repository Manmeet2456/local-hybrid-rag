import os
from pathlib import Path

# Redirect all AI/ML cache directories to D:\cache
CACHE_DIR = Path("D:/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(CACHE_DIR / "huggingface")
os.environ["HUGGINGFACE_HUB_CACHE"] = str(CACHE_DIR / "huggingface" / "hub")
os.environ["TRANSFORMERS_CACHE"] = str(CACHE_DIR / "huggingface" / "transformers")
os.environ["TORCH_HOME"] = str(CACHE_DIR / "torch")
os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(CACHE_DIR / "sentence_transformers")
os.environ["DOCLING_CACHE_DIR"] = str(CACHE_DIR / "docling")
os.environ["EASYOCR_MODULE_PATH"] = str(CACHE_DIR / "easyocr")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.upload import router as upload_router
from api.chat import router as chat_router
from api.document import router as document_router

app = FastAPI(title="Local Hybrid RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Rag API"}

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)