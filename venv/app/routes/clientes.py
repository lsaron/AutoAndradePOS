from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.clientes import Cliente
from app.models.carros import Carro

router = APIRouter()

@router.get("/clientes/{id_cliente}")
def obtener_cliente_con_carros(id_cliente: int, db: Session = Depends(get_db)):
    # Buscar el cliente por ID
    cliente = db.query(Cliente).filter(Cliente.id == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Obtener todos los carros asociados al cliente
    carros = db.query(Carro).filter(Carro.id_cliente_actual == id_cliente).all()
    lista_carros = [
        {
            "matricula": carro.matricula,
            "marca": carro.marca,
            "modelo": carro.modelo,
            "anio": carro.anio
        }
        for carro in carros
    ]

    return {
        "id": cliente.id,
        "nombre": cliente.nombre,
        "correo": cliente.correo,
        "telefono": cliente.telefono,
        "carros": lista_carros
    }
