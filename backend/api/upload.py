import os
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException

from ingestion.pipeline import ingest_pdf

router = APIRouter(prefix="/upload", tags=["upload"])
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("")
@router.post("/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf") and file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are allowed."
        )

    document_id = str(uuid4())
    filename = f"{document_id}.pdf"
    file_path = UPLOAD_DIR / filename
    
    try:
        content = await file.read()
        with open(file_path, "wb") as buffer:
            buffer.write(content)
            
        result = ingest_pdf(str(file_path.resolve()), document_id=document_id, filename=file.filename)
        
        return {
            "message": "PDF indexed successfully", 
            "filename": file.filename, 
            "document_id": document_id,
            **result
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {str(e)}"
        )