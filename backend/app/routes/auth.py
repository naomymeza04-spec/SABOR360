from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    correo: str
    contrasena: str


class LoginResponse(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    token: str


@router.post("/login", response_model=LoginResponse)
def login(datos: LoginRequest):
    raise HTTPException(status_code=501, detail="Login no implementado todavía")

    # TODO: validar credenciales contra la tabla Usuario y devolver JWT