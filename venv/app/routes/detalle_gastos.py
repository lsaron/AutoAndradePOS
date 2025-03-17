from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.detalle_gastos import DetalleGasto
from app.schemas.detalle_gastos import DetalleGastoSchema
router = APIRouter()

@router.get("/detalle_gastos/{id_trabajo}")
def obtener_gastos_por_trabajo(id_trabajo: int, db: Session = Depends(get_db)):
    from app.schemas.detalle_gastos import DetalleGastoSchema  

    detalles = db.query(DetalleGasto).filter(DetalleGasto.id_trabajo == id_trabajo).all()
    if not detalles:
        raise HTTPException(status_code=404, detail="No hay gastos para este trabajo")
    return detalles
@router.put("/detalle_gastos/{id_gasto}")
def actualizar_detalle_gasto(id_gasto: int, gasto_update: DetalleGastoSchema, db: Session = Depends(get_db)):
    gasto_db = db.query(DetalleGasto).filter(DetalleGasto.id == id_gasto).first()
    if not gasto_db:
        raise HTTPException(status_code=404, detail="Detalle de gasto no encontrado")

    # ✅ Actualizar la información del gasto
    gasto_db.descripcion = gasto_update.descripcion
    gasto_db.monto = gasto_update.monto

    db.commit()
    return {"message": "Detalle de gasto actualizado correctamente"}
