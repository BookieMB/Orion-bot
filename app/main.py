from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routers import auth, chat, integrations, upload, history

app = FastAPI(title="LLM MVP (FastAPI)")

# Paths
BASE_DIR = Path(__file__).resolve().parent           # app/
STATIC_DIR = BASE_DIR / "static"                     # app/static

# Mount static folder for chat-specific assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Root route serves chat.html
@app.get("/")
def root():
    chat_file = STATIC_DIR / "chat.html"
    if not chat_file.exists():
        return {"error": "chat.html not found"}
    return FileResponse(chat_file)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(history.router, prefix="/history", tags=["history"])
