from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Trabajo(Base):
    __tablename__ = "trabajos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    matricula_carro = Column(String(20), ForeignKey("carros.matricula", ondelete="CASCADE"))  # ✅ Referencia a matrícula
    descripcion = Column(String(255), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    costo = Column(Integer, nullable=False)

    # ✅ Relación con Carro (cada trabajo pertenece a un carro específico)
    carro = relationship("Carro", back_populates="trabajos")

    # ✅ Relación con Detalles de Gastos (un trabajo puede tener múltiples gastos)
    detalles_gastos = relationship("DetalleGasto", back_populates="trabajo", cascade="all, delete-orphan")  # 👈 AGREGA ESTO
