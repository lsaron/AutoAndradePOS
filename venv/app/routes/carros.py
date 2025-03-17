from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.carros import Carro
from app.models.historial_duenos import HistorialDueno
from app.models.clientes import Cliente
from app.schemas.carros import CarroSchema

router = APIRouter()

# ✅ OBTENER HISTORIAL COMPLETO DE UN CARRO (DUEÑOS Y TRABAJOS)
@router.get("/carros/historial/{matricula}")
def obtener_historial_carro(matricula: str, db: Session = Depends(get_db)):
    carro = db.query(Carro).filter(Carro.matricula == matricula).first()
    if not carro:
        raise HTTPException(status_code=404, detail="Carro no encontrado")

    # ✅ Obtener el dueño actual
    cliente_actual = db.query(Cliente).filter(Cliente.id_nacional == carro.id_cliente_actual).first()
    dueno_actual = {
        "id_cliente": cliente_actual.id_nacional if cliente_actual else None,
        "nombre": cliente_actual.nombre if cliente_actual else "Sin dueño"
    }

    # ✅ Obtener historial de dueños con una sola consulta optimizada
    historial_duenos = (
        db.query(HistorialDueno, Cliente.nombre)
        .outerjoin(Cliente, HistorialDueno.id_cliente == Cliente.id_nacional)
        .filter(HistorialDueno.matricula_carro == carro.matricula)
        .all()
    )

    lista_duenos = [
        {
            "id_cliente": d.HistorialDueno.id_cliente,
            "nombre": d.nombre if d.nombre else "Desconocido",
            "fecha_inicio": d.HistorialDueno.fecha_inicio,
            "fecha_fin": d.HistorialDueno.fecha_fin
        }
        for d in historial_duenos
    ]

    return {
        "matricula": carro.matricula,
        "marca": carro.marca,
        "modelo": carro.modelo,
        "anio": carro.anio,
        "dueno_actual": dueno_actual,  # ✅ Ahora muestra ID y nombre
        "historial_duenos": lista_duenos  # ✅ Optimizado
    }


# ✅ CREAR UN NUEVO CARRO
@router.post("/carros/")
def crear_carro(carro: CarroSchema, db: Session = Depends(get_db)):
    # Verificar si ya existe un carro con esa matrícula
    carro_existente = db.query(Carro).filter(Carro.matricula == carro.matricula).first()
    if carro_existente:
        raise HTTPException(status_code=400, detail="Ya existe un carro con esta matrícula")

    # ✅ Verificar que el cliente dueño del carro exista
    if carro.id_cliente_actual:
        cliente_existente = db.query(Cliente).filter(Cliente.id_nacional == carro.id_cliente_actual).first()
        if not cliente_existente:
            raise HTTPException(status_code=400, detail="El cliente especificado no existe")

    # ✅ Crear el nuevo carro
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
            matricula_carro=nuevo_carro.matricula,  # ✅ Se usa matrícula
            id_cliente=carro.id_cliente_actual,
            fecha_inicio=datetime.utcnow(),
            fecha_fin=None  # No tiene fecha de fin hasta que cambie de dueño
        )
        db.add(historial)

    db.commit()
    db.refresh(nuevo_carro)
    return {"message": "Carro creado correctamente", "carro": nuevo_carro}
