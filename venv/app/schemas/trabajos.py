from pydantic import BaseModel
from typing import List
from datetime import datetime

class DetalleGastoSchema(BaseModel):
    descripcion: str
    monto: int

class TrabajoSchema(BaseModel):
    matricula_carro: str  # ✅ Ahora se usa la matrícula en lugar del ID
    descripcion: str
    fecha: datetime
    costo: int
    detalle_gastos: List[DetalleGastoSchema]  # ✅ Se incluyen los gastos
