from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

HISTORY_FILE = "chat_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@router.get("/chat/history")
def get_history():
    return {"history": load_history()}

@router.delete("/chat/history/{chat_id}")
def delete_chat(chat_id: int):
    history = load_history()
    if chat_id < 0 or chat_id >= len(history):
        raise HTTPException(status_code=404, detail="Chat not found")
    history.pop(chat_id)
    save_history(history)
    return {"status": "success"}
