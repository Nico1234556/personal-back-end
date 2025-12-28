from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import UserLogin

router = APIRouter()

@router.post("/login")
def login(credentials: UserLogin, session: Session = Depends(get_session)):
    # Buscamos al usuario por email
    user = session.exec(select(User).where(User.email == credentials.email)).first()
    
    # Si no existe O la contraseña no coincide
    if not user or user.password != credentials.password:  # <--- CORREGIDO AQUÍ
        raise HTTPException(status_code=400, detail="Email o contraseña incorrectos")
    
    return {"message": "Login exitoso", "user_id": user.id, "username": user.username}