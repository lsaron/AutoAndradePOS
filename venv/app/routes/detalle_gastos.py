from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.detalle_gastos import DetalleGasto

router = APIRouter()

@router.get("/detalle_gastos/{id_trabajo}")
def obtener_gastos_por_trabajo(id_trabajo: int, db: Session = Depends(get_db)):
    from app.schemas.detalle_gastos import DetalleGastoSchema  # 👈 Mover import aquí

    detalles = db.query(DetalleGasto).filter(DetalleGasto.id_trabajo == id_trabajo).all()
    if not detalles:
        raise HTTPException(status_code=404, detail="No hay gastos para este trabajo")
    return detalles
