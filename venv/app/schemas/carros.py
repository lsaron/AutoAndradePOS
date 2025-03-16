from pydantic import BaseModel
from typing import Optional

class CarroSchema(BaseModel):
    matricula: str
    marca: str
    modelo: str
    anio: int
    id_cliente_actual: Optional[int]

    class Config:
        orm_mode = True
