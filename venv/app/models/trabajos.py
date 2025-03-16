from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class Trabajo(Base):
    __tablename__ = "trabajos"

    id = Column(Integer, primary_key=True, index=True)
    id_carro = Column(Integer, ForeignKey("carros.id"))
    descripcion = Column(String(255))
    fecha = Column(DateTime, default=datetime.utcnow)
    costo = Column(Integer)

    # Relación con Carro
    carro = relationship("Carro", back_populates="trabajos")

    # Relación con Detalles de Gastos
    detalles_gastos = relationship("DetalleGasto", back_populates="trabajo")

    __table_args__ = {'extend_existing': True}  # Asegura que SQLAlchemy no intente crearla otra vez
