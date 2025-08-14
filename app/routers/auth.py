from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt, os
from datetime import datetime, timedelta
from app.db import get_db, Base, engine
from app.models import User
from app.schemas import RegisterRequest, LoginRequest, TokenResponse

# Create tables if not exist
Base.metadata.create_all(bind=engine)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.getenv("JWT_SECRET", "devsecret")
JWT_ALG = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", "120"))

def create_access_token(sub: str):
    payload = {
        "sub": sub,
        "exp": datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MIN)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=data.username, password_hash=pwd_context.hash(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Registered", "username": user.username}

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not pwd_context.verify(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=str(user.id))
    return TokenResponse(access_token=token)

def get_current_user_id(authorization: str = Header(None)):
    # Very light JWT parse: expecting "Bearer <token>"
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
