from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Carro(Base):
    __tablename__ = "carros"

    matricula = Column(String(20), primary_key=True, unique=True, index=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    anio = Column(Integer, nullable=False)
    id_cliente_actual = Column(String(20), ForeignKey("clientes.id_nacional", ondelete="SET NULL"))

    # ✅ Relación con Cliente (Un carro pertenece a un cliente actual)
    cliente_actual = relationship("Cliente", back_populates="carros")

    # ✅ Relación con Trabajos (Un carro puede tener múltiples trabajos)
    trabajos = relationship("Trabajo", back_populates="carro", cascade="all, delete-orphan")

    # ✅ Relación con Historial de Dueños (Un carro puede haber tenido múltiples dueños)
    historial_duenos = relationship("HistorialDueno", back_populates="carro", cascade="all, delete-orphan")  # 👈 AGREGA ESTO
