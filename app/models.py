from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    password: str  # <--- AQUÍ ESTÁ LA CLAVE: Debe decir password, no hashed_password
    is_active: bool = True