from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.trabajos import Trabajo
from app.models.detalle_gastos import DetalleGasto
from app.models.carros import Carro  # ✅ Importar el modelo de Carro
from app.schemas.trabajos import TrabajoSchema

router = APIRouter()

# ✅ OBTENER TODOS LOS TRABAJOS DE UN CARRO POR MATRÍCULA
@router.get("/trabajos/{matricula_carro}")
def obtener_trabajos_por_carro(matricula_carro: str, db: Session = Depends(get_db)):
    trabajos = db.query(Trabajo).filter(Trabajo.matricula_carro == matricula_carro).all()
    if not trabajos:
        raise HTTPException(status_code=404, detail="No hay trabajos registrados para este carro")
    
    historial_trabajos = []
    
    for t in trabajos:
        detalles_gastos = db.query(DetalleGasto).filter(DetalleGasto.id_trabajo == t.id).all()
        lista_gastos = [{"descripcion": d.descripcion, "monto": d.monto} for d in detalles_gastos]

        historial_trabajos.append({
            "descripcion": t.descripcion,
            "fecha": t.fecha,
            "costo": t.costo,
            "detalle_gastos": lista_gastos  # ✅ Se agregan los gastos del trabajo
        })

    return {
        "matricula_carro": matricula_carro,
        "historial_trabajos": historial_trabajos
    }

# ✅ CREAR UN NUEVO TRABAJO CON GASTOS
@router.post("/trabajos/")
def crear_trabajo(trabajo: TrabajoSchema, db: Session = Depends(get_db)):
    # ✅ Verificar que el carro existe antes de registrar un trabajo
    carro_existente = db.query(Carro).filter(Carro.matricula == trabajo.matricula_carro).first()
    if not carro_existente:
        raise HTTPException(status_code=400, detail="El carro especificado no existe")

    # ✅ Crear el trabajo
    nuevo_trabajo = Trabajo(
        matricula_carro=trabajo.matricula_carro,  # 👈 Se asigna la matrícula del carro
        descripcion=trabajo.descripcion,
        fecha=trabajo.fecha,
        costo=trabajo.costo
    )
    db.add(nuevo_trabajo)
    db.commit()
    db.refresh(nuevo_trabajo)

    # ✅ Agregar los gastos relacionados (solo si se envían gastos)
    if trabajo.detalle_gastos:
        for gasto in trabajo.detalle_gastos:
            nuevo_gasto = DetalleGasto(
                id_trabajo=nuevo_trabajo.id,
                descripcion=gasto.descripcion,
                monto=gasto.monto
            )
            db.add(nuevo_gasto)

    db.commit()
    return {"message": "Trabajo creado con sus gastos correctamente"}
