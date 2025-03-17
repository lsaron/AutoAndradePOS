from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.carros import Carro
from app.models.historial_duenos import HistorialDueno
from app.schemas.carros import CarroSchema

router = APIRouter()

# ✅ CREAR UN NUEVO CARRO
@router.post("/carros/")
def crear_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    # Verificar si ya existe un carro con esa matrícula
    carro_existente = db.query(Carro).filter(Carro.matricula == carro.matricula).first()
    if carro_existente:
        raise HTTPException(status_code=400, detail="Ya existe un carro con esta matrícula")

    # Crear el nuevo carro
    nuevo_carro = Carro(
        matricula=carro.matricula,
        marca=carro.marca,
        modelo=carro.modelo,
        anio=carro.anio,
        id_cliente_actual=carro.id_cliente_actual  # Dueño actual si se proporciona
    )
    db.add(nuevo_carro)

    # ✅ Si el carro tiene un dueño al crearlo, registrar en historial_duenos
    if carro.id_cliente_actual:
        historial = HistorialDueno(
            id_carro=nuevo_carro.matricula,  # Se usa matrícula en lugar de ID
            id_cliente=carro.id_cliente_actual,
            fecha_inicio=datetime.utcnow(),
            fecha_fin=None  # No tiene fecha de fin hasta que cambie de dueño
        )
        db.add(historial)

    db.commit()
    db.refresh(nuevo_carro)
    return {"message": "Carro creado correctamente", "carro": nuevo_carro}
