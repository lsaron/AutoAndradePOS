from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class DetalleGasto(Base):
    __tablename__ = "detalle_gastos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajo = Column(Integer, ForeignKey("trabajos.id", ondelete="CASCADE"))  # ✅ Referencia a trabajos
    descripcion = Column(String(255), nullable=False)
    monto = Column(Integer, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    # ✅ Relación con Trabajo
    trabajo = relationship("Trabajo", back_populates="detalles_gastos")  # 👈 AGREGA ESTO
