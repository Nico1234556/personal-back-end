from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserPublic

router = APIRouter()

# 1. CREAR USUARIO (Registrarse)
@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Verificamos si el usuario ya existe
    user_exists = session.exec(select(User).where(User.email == user.email)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Creamos el usuario (Sin encriptar nada, directo)
    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password, # Guardamos "123456" tal cual
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# 2. LEER USUARIOS (Ver lista de todos)
@router.get("/", response_model=list[UserPublic])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users