from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_nacional = Column(String(20), primary_key=True, unique=True, index=True)  # ✅ Clave primaria basada en ID nacional
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=False)

    # ✅ Relación con Carros (un cliente puede tener varios carros)
    carros = relationship("Carro", back_populates="cliente_actual", cascade="all, delete-orphan")
