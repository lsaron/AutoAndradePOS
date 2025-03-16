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

    carro = relationship("Carro", back_populates="trabajos")
detalle_gastos = relationship("DetalleGasto", back_populates="trabajo")
