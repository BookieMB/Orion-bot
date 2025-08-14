from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.db import get_db, Base, engine
from app.models import Message
from app.schemas import ChatRequest, ChatHistoryResponse, ChatMessage
from app.llm import call_llm

# Ensure tables exist
Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/", response_model=ChatMessage)
def chat(
    req: ChatRequest,
    db: Session = Depends(get_db)
):
    # TEMP: hardcoded test user
    user_id = 1

    # Save user message
    m_user = Message(user_id=user_id, role="user", content=req.prompt)
    db.add(m_user)
    db.commit()
    db.refresh(m_user)

    try:
        # Build full prompt
        full_prompt = f"{req.system}\n\nUser: {req.prompt}" if req.system else req.prompt
        
        # Call Gemini via your LLM helper
        reply = call_llm(prompt=full_prompt)
        
        if not reply or not isinstance(reply, str):
            raise ValueError("Empty or invalid response from LLM.")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM Error: {e}")

    # Save assistant message
    m_assistant = Message(user_id=user_id, role="assistant", content=reply)
    db.add(m_assistant)
    db.commit()
    db.refresh(m_assistant)

    # Return assistant reply
    return ChatMessage(role="assistant", content=reply)


@router.get("/history", response_model=ChatHistoryResponse)
def history(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    # TEMP: hardcoded test user
    user_id = 1

    msgs = (
        db.query(Message)
        .filter(Message.user_id == user_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    out = [ChatMessage(role=m.role, content=m.content) for m in reversed(msgs)]
    return ChatHistoryResponse(history=out)


# 🗑 Delete a single chat message by ID
@router.delete("/delete/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db)
):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")

    db.delete(msg)
    db.commit()
    return {"message": f"Message {message_id} deleted successfully"}


# 🗑 Delete all chat history for the user
@router.delete("/delete_all")
def delete_all_messages(
    db: Session = Depends(get_db)
):
    # TEMP: hardcoded test user
    user_id = 1

    deleted_count = db.query(Message).filter(Message.user_id == user_id).delete()
    db.commit()
    return {"message": f"Deleted {deleted_count} messages"}


# 🗑 Clear history (shortcut endpoint)
@router.delete("/history/clear")
def clear_history(
    db: Session = Depends(get_db)
):
    # TEMP: replace with real user auth later
    user_id = 1
    deleted = db.query(Message).filter(Message.user_id == user_id).delete()
    db.commit()
    return {"status": "ok", "deleted_count": deleted}
