from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Importamos la base desde database.py

class Carro(Base):
    __tablename__ = "carros"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(20), unique=True, index=True)
    marca = Column(String(50))
    modelo = Column(String(50))
    anio = Column(Integer)
    id_cliente_actual = Column(Integer, ForeignKey("clientes.id"))

    cliente_actual = relationship("Cliente", back_populates="carros")
    trabajos = relationship("Trabajo", back_populates="carro")
