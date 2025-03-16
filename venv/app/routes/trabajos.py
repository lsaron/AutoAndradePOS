from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.trabajos import Trabajo
from app.schemas.trabajos import TrabajoSchema
from app.models.carros import Carro

router = APIRouter()

@router.get("/trabajos/{id_carro}")
def obtener_trabajos_por_carro(id_carro: int, db: Session = Depends(get_db)):
    trabajos = db.query(Trabajo).filter(Trabajo.id_carro == id_carro).all()
    if not trabajos:
        raise HTTPException(status_code=404, detail="No hay trabajos registrados para este carro")
    return trabajos
