from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrabajoSchema(BaseModel):
    id_carro: int
    descripcion: str
    fecha: Optional[datetime] = None
    costo: float

    class Config:
        orm_mode = True
