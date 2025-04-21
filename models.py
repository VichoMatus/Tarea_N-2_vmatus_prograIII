from sqlalchemy import Column, Integer, String, Enum, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum as PyEnum

Base = declarative_base()

class EstadoVuelo(PyEnum):
    programado = "programado"
    emergencia = "emergencia"
    retrasado = "retrasado"

class Vuelo(Base):
    __tablename__ = 'vuelos'

    id = Column(Integer, primary_key=True)
    codigo = Column(String, unique=True)  # Código único del vuelo (Ej: AV2025)
    estado = Column(Enum(EstadoVuelo))  # Estado del vuelo (programado, emergencia, retrasado)
    hora = Column(DateTime, default=datetime.utcnow)  # Hora del vuelo
    origen = Column(String)  # Origen del vuelo (Ej: "Madrid")
    destino = Column(String)  # Destino del vuelo (Ej: "Barcelona")
    
    def __repr__(self):
        return f"<Vuelo(codigo={self.codigo}, estado={self.estado}, hora={self.hora}, origen={self.origen}, destino={self.destino})>"
