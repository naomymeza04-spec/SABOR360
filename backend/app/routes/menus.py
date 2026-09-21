from fastapi import APIRouter

router = APIRouter()


@router.get("")
def listar():
    return {"mensaje": "Listar menús - pendiente de implementar"}


@router.get("/{id_menu}")
def obtener(id_menu: int):
    return {"mensaje": f"Obtener menú {id_menu} - pendiente de implementar"}


@router.post("")
def crear():
    return {"mensaje": "Crear menú - pendiente de implementar"}