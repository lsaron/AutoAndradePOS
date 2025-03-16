from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .database import Base

class DetalleGasto(Base):
    __tablename__ = "detalle_gastos"  # Asegúrate de que coincida con el nombre en MySQL

    id = Column(Integer, primary_key=True, index=True)
    id_trabajo = Column(Integer, ForeignKey("trabajos.id"))
    descripcion = Column(String(255))
    monto = Column(Float)

    trabajo = relationship("Trabajo", back_populates="detalle_gastos")
