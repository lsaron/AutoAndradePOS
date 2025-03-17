from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class HistorialDueno(Base):
    __tablename__ = "historial_duenos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_carro = Column(String(20), ForeignKey("carros.matricula", ondelete="CASCADE"))  # ✅ Usa matrícula en lugar de ID
    id_cliente = Column(String(20), ForeignKey("clientes.id_nacional", ondelete="SET NULL"))  # ✅ Usa id_nacional
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)

    # ✅ Relación con Carro (un carro puede haber tenido varios dueños)
    carro = relationship("Carro", back_populates="historial_duenos")

    # ✅ Relación con Cliente (un cliente puede haber tenido varios carros)
    cliente = relationship("Cliente", back_populates="historial_duenos")
