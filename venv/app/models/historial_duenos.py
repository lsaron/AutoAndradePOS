from sqlalchemy import Column, Integer, ForeignKey, DateTime
from .database import Base
from datetime import datetime

class HistorialDueno(Base):
    __tablename__ = "historial_duenos"

    id = Column(Integer, primary_key=True, index=True)
    id_carro = Column(Integer, ForeignKey("carros.id"))
    id_cliente = Column(Integer, ForeignKey("clientes.id"))
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime, nullable=True)
