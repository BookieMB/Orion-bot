# app/routers/llm_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.llm import call_llm

router = APIRouter()

class PromptRequest(BaseModel):
    message: str

@router.post("/chat")
def chat_with_llm(request: PromptRequest):
    reply = call_llm(request.message)
    return {"reply": reply}
