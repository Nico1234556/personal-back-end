from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import User
from app.schemas import UserCreate, UserPublic, UserUpdate

router = APIRouter()

# 1. CREAR USUARIO (C - Create)
@router.post("/", response_model=UserPublic)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    user_exists = session.exec(select(User).where(User.email == user.email)).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# 2. LEER TODOS (R - Read All)
@router.get("/", response_model=list[UserPublic])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

# 3. LEER UNO SOLO (R - Read One)
@router.get("/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# 4. ACTUALIZAR (U - Update)
@router.patch("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    user_db = session.get(User, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Solo actualizamos los datos que nos enviaron (no nulos)
    user_data = user_update.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_db, key, value)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

# 5. BORRAR (D - Delete)
@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    session.delete(user)
    session.commit()
    return {"ok": True, "message": "Usuario eliminado correctamente"}