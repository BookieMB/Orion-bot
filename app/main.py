from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.routers import auth, chat, integrations, upload, history

app = FastAPI(title="LLM MVP (FastAPI)")

# Paths
BASE_DIR = Path(__file__).resolve().parent       # app/
STATIC_DIR = BASE_DIR / "static"                 # app/static (chat.html, chat.js, styles.css, etc.)

# Mount static folder for CSS, JS, images
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Root route serves chat.html directly
@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "chat.html")

# Optional catch-all route (for SPA if needed)
@app.get("/{full_path:path}")
def catch_all(full_path: str):
    return FileResponse(STATIC_DIR / "chat.html")

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# Allow all CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(history.router, prefix="/history", tags=["history"])
