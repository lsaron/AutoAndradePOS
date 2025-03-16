from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.carros import Carro
from app.schemas.carros import CarroSchema

router = APIRouter()

@router.get("/carros/{matricula}")
def obtener_carro(matricula: str, db: Session = Depends(get_db)):
    carro = db.query(Carro).filter(Carro.matricula == matricula).first()
    if not carro:
        raise HTTPException(status_code=404, detail="Carro no encontrado")
    return carro
