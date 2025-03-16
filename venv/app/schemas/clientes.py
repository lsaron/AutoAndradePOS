from pydantic import BaseModel

class ClienteSchema(BaseModel):
    id: int
    nombre: str
    telefono: str

    class Config:
        orm_mode = True
