from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.historial_duenos import HistorialDueno
from app.schemas.historial_duenos import HistorialDuenoSchema

router = APIRouter()

@router.get("/historial_duenos/{matricula}")
def obtener_historial_duenos(matricula: str, db: Session = Depends(get_db)):
    historial = db.query(HistorialDueno).filter(HistorialDueno.matricula_carro == matricula).all()
    if not historial:
        raise HTTPException(status_code=404, detail="No hay historial de dueños para este carro")
    return historial
