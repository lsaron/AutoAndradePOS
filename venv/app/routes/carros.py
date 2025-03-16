from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.carros import Carro
from app.models.trabajos import Trabajo
from app.models.historial_duenos import HistorialDueno
from app.models.clientes import Cliente

router = APIRouter()

@router.get("/carros/historial/{matricula}")
def obtener_historial_carro(matricula: str, db: Session = Depends(get_db)):
    # Buscar el carro por matrícula
    carro = db.query(Carro).filter(Carro.matricula == matricula).first()
    if not carro:
        raise HTTPException(status_code=404, detail="Carro no encontrado")

    # Obtener el dueño actual
    cliente_actual = db.query(Cliente).filter(Cliente.id == carro.id_cliente_actual).first()

    # Obtener el historial de dueños
    historial_duenos = db.query(HistorialDueno).filter(HistorialDueno.id_carro == carro.id).all()
    duenos = [
        {
            "id_cliente": dueno.id_cliente,
            "nombre": db.query(Cliente).filter(Cliente.id == dueno.id_cliente).first().nombre,
            "fecha_inicio": dueno.fecha_inicio,
            "fecha_fin": dueno.fecha_fin
        }
        for dueno in historial_duenos
    ]

    # Obtener el historial de trabajos
    trabajos = db.query(Trabajo).filter(Trabajo.id_carro == carro.id).all()
    historial_trabajos = [
        {
            "descripcion": trabajo.descripcion,
            "fecha": trabajo.fecha,
            "costo": trabajo.costo
        }
        for trabajo in trabajos
    ]

    return {
        "matricula": carro.matricula,
        "marca": carro.marca,
        "modelo": carro.modelo,
        "anio": carro.anio,
        "dueno_actual": {
            "id_cliente": cliente_actual.id if cliente_actual else None,
            "nombre": cliente_actual.nombre if cliente_actual else "Sin dueño asignado"
        },
        "historial_duenos": duenos,
        "historial_trabajos": historial_trabajos
    }
