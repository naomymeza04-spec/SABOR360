from fastapi import APIRouter

router = APIRouter()


@router.get("/diario")
def reporte_diario():
    return {"mensaje": "Reporte diario - pendiente de implementar"}


@router.get("/por-usuario/{id_usuario}")
def reporte_por_usuario(id_usuario: int):
    return {"mensaje": f"Reporte del usuario {id_usuario} - pendiente de implementar"}