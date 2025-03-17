from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.clientes import Cliente
from app.models.carros import Carro
from app.schemas.clientes import ClienteSchema, ClienteConCarrosSchema

router = APIRouter()

# ✅ CREAR UN CLIENTE
@router.post("/clientes/")
def crear_cliente(cliente: ClienteSchema, db: Session = Depends(get_db)):
    # Verificar si el cliente ya existe
    cliente_existente = db.query(Cliente).filter(Cliente.id_nacional == cliente.id_nacional).first()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="El cliente con este ID nacional ya existe")

    # Crear nuevo cliente
    nuevo_cliente = Cliente(
        id_nacional=cliente.id_nacional,
        nombre=cliente.nombre,
        correo=cliente.correo,
        telefono=cliente.telefono
    )
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)

    return {"message": "Cliente creado correctamente", "cliente": nuevo_cliente}

# ✅ OBTENER UN CLIENTE CON SUS CARROS ASOCIADOS
@router.get("/clientes/{id_nacional}", response_model=ClienteConCarrosSchema)
def obtener_cliente_con_carros(id_nacional: str, db: Session = Depends(get_db)):
    # Buscar el cliente por ID Nacional
    cliente = db.query(Cliente).filter(Cliente.id_nacional == id_nacional).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Obtener todos los carros asociados al cliente
    carros = db.query(Carro).filter(Carro.id_cliente_actual == id_nacional).all()
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
        "id_nacional": cliente.id_nacional,
        "nombre": cliente.nombre,
        "correo": cliente.correo,
        "telefono": cliente.telefono,
        "carros": lista_carros
    }
