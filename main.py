from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import auth, users

# 1. Configuración de arranque (Lifespan)
# Esto reemplaza al antiguo @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # Crea la base de datos al iniciar
    yield

# 2. Inicializar la aplicación
app = FastAPI(title="Mi Backend Personal", lifespan=lifespan)

# 3. Configuración de CORS
# Permite que tu Frontend (Next.js en puerto 3000) hable con este Backend
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # <--- CAMBIO CLAVE: El asterisco permite todo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Conectar las rutas (Los archivos que creamos antes)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# 5. Ruta de prueba (Home)
@app.get("/")
def read_root():
    return {"message": "¡El Backend está vivo! 🚀 Ve a /docs para probarlo."}