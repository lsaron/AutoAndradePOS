from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    telefono = Column(String(15))

    carros = relationship("Carro", back_populates="cliente_actual")
