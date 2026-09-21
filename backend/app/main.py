from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, consumos, inventario, menus, platos, reportes, usuarios

app = FastAPI(
    title="Sabor 360 API",
    description="Sistema de gestión y control para restaurante mediante código QR.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(platos.router, prefix="/api/platos", tags=["Platos"])
app.include_router(menus.router, prefix="/api/menus", tags=["Menús"])
app.include_router(inventario.router, prefix="/api/inventario", tags=["Inventario"])
app.include_router(consumos.router, prefix="/api/consumos", tags=["Consumos"])
app.include_router(reportes.router, prefix="/api/reportes", tags=["Reportes"])


@app.get("/")
def raiz():
    return {"mensaje": "Sabor 360 API funcionando"}