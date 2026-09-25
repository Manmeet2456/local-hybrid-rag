from fastapi import APIRouter
from db.qdrant import list_documents, delete_document

router = APIRouter(prefix="/documents", tags=["documents"])

@router.get("")
@router.get("/")
def get_documents():
    return list_documents()

@router.delete("/{document_id}")
def remove_document(document_id: str):
    delete_document(document_id)
    return {"message": "Document deleted"}