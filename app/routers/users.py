from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database import get_session
from app.models import User, UserCreate, UserRead
from app.security import get_password_hash
from app.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    user_db = User.from_orm(user)
    user_db.hashed_password = get_password_hash(user.password)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserRead])
def read_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return session.exec(select(User)).all()