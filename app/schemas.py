from pydantic import BaseModel

# Esto valida los datos cuando ALGUIEN SE REGISTRA
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Esto es lo que devolvemos al frontend (Ocultamos la password)
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

# Esto valida los datos cuando ALGUIEN HACE LOGIN
class UserLogin(BaseModel):
    email: str
    password: str