from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import auth, users
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Mi Backend Personal")
# Configuración de CORS para permitir que el frontend (React) nos hable 
origins = [
    "http://localhost:3000", # El puerto donde correrá Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Aquí conectamos las piezas
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])