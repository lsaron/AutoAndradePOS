from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Carro(Base):
    __tablename__ = "carros"

    matricula = Column(String(20), primary_key=True, unique=True, index=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    anio = Column(Integer)
    id_cliente_actual = Column(String(20), ForeignKey("clientes.id_nacional", ondelete="SET NULL"))

    # ✅ Relación con Cliente
    cliente_actual = relationship("Cliente", back_populates="carros")
    trabajos = relationship("Trabajo", back_populates="carro", cascade="all, delete-orphan")  # 👈 Agregar esto si falta

    # ✅ Relación con Historial de Dueños (basado en la matrícula)
    historial_duenos = relationship("HistorialDueno", back_populates="carro", cascade="all, delete-orphan")