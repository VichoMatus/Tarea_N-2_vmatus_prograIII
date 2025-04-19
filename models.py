from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum as PyEnum

# Base de datos SQLAlchemy
Base = declarative_base()

class EstadoVuelo(PyEnum):
    PROGRAMADO = "programado"
    EMERGENCIA = "emergencia"
    RETRASADO = "retrasado"

# Modelo de Vuelo
class Vuelo(Base):
    __tablename__ = 'vuelos'
    
    id = Column(Integer, primary_key=True, index=True)  # Identificador único
    codigo = Column(String, unique=True, index=True)    # Código del vuelo
    estado = Column(Enum(EstadoVuelo))                  # Estado del vuelo
    hora = Column(DateTime, default=datetime.utcnow)    # Hora del vuelo
    origen = Column(String)                             # Ciudad de origen
    destino = Column(String)                            # Ciudad de destino

    # Relación con la tabla Asiento
    asientos = relationship("Asiento", back_populates="vuelo")

    # Relación con la tabla Reserva
    reservas = relationship("Reserva", back_populates="vuelo")

# Modelo de Asiento
class Asiento(Base):
    __tablename__ = 'asientos'
    
    id = Column(Integer, primary_key=True, index=True)  # ID único
    vuelo_id = Column(Integer, ForeignKey('vuelos.id'))  # ID del vuelo asociado
    asiento_numero = Column(String, index=True)          # Número de asiento
    
    # Relación con la tabla Vuelo
    vuelo = relationship("Vuelo", back_populates="asientos")
    
    # Relación con la tabla Reserva
    reservas = relationship("Reserva", back_populates="asiento")

# Modelo de Cliente
class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefono = Column(String)
    
    # Relación con reservas
    reservas = relationship("Reserva", back_populates="cliente")

# Modelo de Reserva
class Reserva(Base):
    __tablename__ = 'reservas'
    
    id = Column(Integer, primary_key=True, index=True)  # ID único
    cliente_id = Column(Integer, ForeignKey('clientes.id'))  # Cliente que realizó la reserva
    asiento_id = Column(Integer, ForeignKey('asientos.id'))  # Asiento reservado
    vuelo_id = Column(Integer, ForeignKey('vuelos.id'))  # Vuelo reservado
    fecha_reserva = Column(DateTime, default=datetime.utcnow)  # Fecha de la reserva
    
    # Relación con el Cliente
    cliente = relationship("Cliente", back_populates="reservas")
    
    # Relación con el Asiento
    asiento = relationship("Asiento", back_populates="reservas")
    
    # Relación con el Vuelo
    vuelo = relationship("Vuelo", back_populates="reservas")

