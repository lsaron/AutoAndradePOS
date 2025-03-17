from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class DetalleGasto(Base):
    __tablename__ = "detalle_gastos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajo = Column(Integer, ForeignKey("trabajos.id", ondelete="CASCADE"))  # ✅ Relación con trabajos
    descripcion = Column(String(255), nullable=False)  # ✅ Descripción del gasto
    monto = Column(Integer, nullable=False)  # ✅ Costo del gasto
    fecha = Column(DateTime, default=datetime.utcnow)

    # ✅ Relación con Trabajo (Un trabajo puede tener múltiples gastos)
    trabajo = relationship("Trabajo", back_populates="detalle_gastos")
