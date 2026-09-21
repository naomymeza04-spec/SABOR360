from fastapi import APIRouter

router = APIRouter()


@router.get("")
def listar():
    return {"mensaje": "Listar platos - pendiente de implementar"}


@router.get("/{id_plato}")
def obtener(id_plato: int):
    return {"mensaje": f"Obtener plato {id_plato} - pendiente de implementar"}


@router.post("")
def crear():
    return {"mensaje": "Crear plato - pendiente de implementar"}