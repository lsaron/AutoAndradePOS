from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class DetalleGasto(Base):
    __tablename__ = "detalles_gastos"

    id = Column(Integer, primary_key=True, index=True)
    id_trabajo = Column(Integer, ForeignKey("trabajos.id"))
    descripcion = Column(String(255))
    monto = Column(Float)

    # Relación con la tabla trabajos
    trabajo = relationship("Trabajo", back_populates="detalles_gastos")
