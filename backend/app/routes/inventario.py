from fastapi import APIRouter

router = APIRouter()


@router.get("")
def listar():
    return {"mensaje": "Listar inventario - pendiente de implementar"}


@router.post("")
def registrar():
    return {"mensaje": "Registrar producto - pendiente de implementar"}


@router.post("/{id_inventario}/movimientos")
def registrar_movimiento(id_inventario: int):
    return {"mensaje": f"Movimiento para inventario {id_inventario} - pendiente de implementar"}