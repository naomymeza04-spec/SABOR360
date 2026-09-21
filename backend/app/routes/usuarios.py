from fastapi import APIRouter

router = APIRouter()


@router.get("")
def listar():
    return {"mensaje": "Listar usuarios - pendiente de implementar"}


@router.get("/{id_usuario}")
def obtener(id_usuario: int):
    return {"mensaje": f"Obtener usuario {id_usuario} - pendiente de implementar"}


@router.post("")
def crear():
    return {"mensaje": "Crear usuario - pendiente de implementar"}