from pydantic import BaseModel
from fastapi import APIRouter
from rag.pipeline import ask

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    question: str
    session_id: str

@router.post("")
@router.post("/")
def chat_endpoint(request: ChatRequest):
    answer = ask(request.question, session_id=request.session_id)
    return answer