from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteSchema(BaseModel):
    id: int
    nombre: str
    correo: Optional[EmailStr] = None
    telefono: str  # Eliminamos "celular", solo usamos "telefono"

    class Config:
        from_attributes = True
