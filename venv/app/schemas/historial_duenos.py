from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistorialDuenoSchema(BaseModel):
    id_carro: int
    id_cliente: int
    fecha_inicio: Optional[datetime]
    fecha_fin: Optional[datetime] = None

    class Config:
        orm_mode = True
