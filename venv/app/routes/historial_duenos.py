from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.carros import Carro
from app.models.historial_duenos import HistorialDueno
from app.models.clientes import Cliente
from app.schemas.carros import CarroSchema

router = APIRouter()

@router.put("/carros/{matricula}/dueno")
def actualizar_dueno_carro(matricula: str, data: dict, db: Session = Depends(get_db)):
    # Verificar si el carro existe
    carro_db = db.query(Carro).filter(Carro.matricula == matricula).first()
    if not carro_db:
        raise HTTPException(status_code=404, detail="Carro no encontrado")

    # Verificar que el request tenga el nuevo dueño
    nuevo_dueno_id = data.get("id_cliente_actual")
    if not nuevo_dueno_id:
        raise HTTPException(status_code=400, detail="Debes proporcionar un nuevo dueño")

    # Verificar si el nuevo dueño existe
    cliente_existente = db.query(Cliente).filter(Cliente.id_nacional == nuevo_dueno_id).first()
    if not cliente_existente:
        raise HTTPException(status_code=400, detail="El nuevo dueño especificado no existe")

    # Si el carro tenía un dueño anterior, actualizar historial
    if carro_db.id_cliente_actual:
        historial_anterior = HistorialDueno(
            matricula_carro=carro_db.matricula,
            id_cliente=carro_db.id_cliente_actual,  # Guardar el dueño anterior
            fecha_inicio=carro_db.fecha_ultima_asignacion,
            fecha_fin=datetime.utcnow()  # Registrar la fecha en la que deja de ser dueño
        )
        db.add(historial_anterior)

    # ✅ Actualizar el dueño actual en la tabla `carros`
    carro_db.id_cliente_actual = nuevo_dueno_id
    carro_db.fecha_ultima_asignacion = datetime.utcnow()  # Guardar fecha de cambio

    # ✅ Agregar el nuevo dueño al historial
    historial_nuevo = HistorialDueno(
        matricula_carro=carro_db.matricula,
        id_cliente=nuevo_dueno_id,
        fecha_inicio=datetime.utcnow(),
        fecha_fin=None  # Aún es el dueño actual
    )
    db.add(historial_nuevo)

    db.commit()
    return {"message": "Dueño del carro actualizado correctamente"}