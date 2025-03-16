from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.historial_duenos import HistorialDueno
from app.schemas.historial_duenos import HistorialDuenoSchema

router = APIRouter()

@router.get("/historial_duenos/{id_carro}")
def obtener_historial_duenos(id_carro: int, db: Session = Depends(get_db)):
    historial = db.query(HistorialDueno).filter(HistorialDueno.id_carro == id_carro).all()
    if not historial:
        raise HTTPException(status_code=404, detail="No hay historial de dueños para este carro")
    return historial
