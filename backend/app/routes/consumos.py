from fastapi import APIRouter

router = APIRouter()


@router.get("")
def listar():
    return {"mensaje": "Listar consumos - pendiente de implementar"}


@router.post("")
def registrar():
    return {"mensaje": "Registrar consumo - pendiente de implementar"}