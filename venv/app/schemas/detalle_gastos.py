from pydantic import BaseModel
from typing import Optional

class DetalleGastoSchema(BaseModel):
    id_trabajo: int
    descripcion: str
    monto: float

    class Config:
        orm_mode = True
