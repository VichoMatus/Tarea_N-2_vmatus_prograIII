from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from models import Base, Vuelo, Asiento, Cliente, Reserva, EstadoVuelo
from typing import List
from datetime import datetime

# Configuración de la aplicación FastAPI
app = FastAPI()

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./Aeropuerto.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Definir el modelo de datos (sin redefinir las clases)
class VueloBase(BaseModel):
    codigo: str
    estado: EstadoVuelo
    hora: str
    origen: str
    destino: str

class AsientoBase(BaseModel):
    asiento_numero: str
    vuelo_id: int

class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: str

class ReservaBase(BaseModel):
    cliente_id: int
    asiento_id: int
    vuelo_id: int

from datetime import datetime

@app.post("/vuelos")
def crear_vuelo(vuelo: VueloBase):
    try:
        # Convertir la hora del vuelo desde string a datetime
        hora_vuelo = datetime.strptime(vuelo.hora, "%H:%M")
        
        db = SessionLocal()
        vuelo_obj = Vuelo(codigo=vuelo.codigo, estado=vuelo.estado, hora=hora_vuelo, origen=vuelo.origen, destino=vuelo.destino)
        db.add(vuelo_obj)
        db.commit()
        db.refresh(vuelo_obj)
        db.close()
        
        # Formatear la hora al formato deseado (hora:minuto)
        hora_formateada = vuelo_obj.hora.strftime("%H:%M")
        
        return {"mensaje": "Vuelo creado exitosamente", "codigo_vuelo": vuelo_obj.codigo, "hora": hora_formateada}
    except Exception as e:
        db.rollback()  # Deshacer los cambios si algo falla
        db.close()
        raise HTTPException(status_code=500, detail=f"Error al crear el vuelo: {str(e)}")


@app.post("/asientos")
def crear_asiento(asiento: AsientoBase):
    db = SessionLocal()
    asiento_obj = Asiento(asiento_numero=asiento.asiento_numero, vuelo_id=asiento.vuelo_id)
    db.add(asiento_obj)
    db.commit()
    db.refresh(asiento_obj)
    db.close()
    return {"mensaje": "Asiento creado exitosamente", "asiento_numero": asiento_obj.asiento_numero}

@app.post("/clientes")
def crear_cliente(cliente: ClienteBase):
    db = SessionLocal()
    cliente_obj = Cliente(nombre=cliente.nombre, email=cliente.email, telefono=cliente.telefono)
    db.add(cliente_obj)
    db.commit()
    db.refresh(cliente_obj)
    db.close()
    return {"mensaje": "Cliente creado exitosamente", "nombre_cliente": cliente_obj.nombre}

@app.post("/reservas")
def crear_reserva(reserva: ReservaBase):
    db = SessionLocal()
    reserva_obj = Reserva(cliente_id=reserva.cliente_id, asiento_id=reserva.asiento_id, vuelo_id=reserva.vuelo_id)
    db.add(reserva_obj)
    db.commit()
    db.refresh(reserva_obj)
    db.close()
    return {"mensaje": "Reserva realizada exitosamente", "id_reserva": reserva_obj.id}

@app.get("/vuelos/total")
def obtener_total_vuelos():
    db = SessionLocal()
    total_vuelos = db.query(Vuelo).count()
    db.close()
    return {"total_vuelos": total_vuelos}

@app.get("/vuelos/proximo")
def obtener_proximo_vuelo():
    db = SessionLocal()
    vuelo = db.query(Vuelo).order_by(Vuelo.hora).first()
    db.close()
    if vuelo:
        return {"vuelo_codigo": vuelo.codigo, "hora": vuelo.hora}
    raise HTTPException(status_code=404, detail="No hay vuelos programados")

@app.get("/vuelos/{vuelo_id}")
def obtener_vuelo(vuelo_id: int):
    db = SessionLocal()
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    db.close()
    if vuelo:
        return {"vuelo_codigo": vuelo.codigo, "origen": vuelo.origen, "destino": vuelo.destino, "estado": vuelo.estado, "hora": vuelo.hora}
    raise HTTPException(status_code=404, detail="Vuelo no encontrado")

@app.get("/clientes/{cliente_id}")
def obtener_cliente(cliente_id: int):
    db = SessionLocal()
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    db.close()
    if cliente:
        return {"nombre": cliente.nombre, "email": cliente.email, "telefono": cliente.telefono}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.get("/reservas/{reserva_id}")
def obtener_reserva(reserva_id: int):
    db = SessionLocal()
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    db.close()
    if reserva:
        return {"id_reserva": reserva.id, "cliente_id": reserva.cliente_id, "asiento_id": reserva.asiento_id, "vuelo_id": reserva.vuelo_id}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.get("/vuelos/lista")
def obtener_lista_vuelos():
    db = SessionLocal()
    vuelos = db.query(Vuelo).all()
    db.close()
    return {"vuelos": [vuelo.codigo for vuelo in vuelos]}


@app.delete("/vuelos/{posicion}")
def eliminar_vuelo(posicion: int):
    db = SessionLocal()
    vuelo = db.query(Vuelo).filter(Vuelo.id == posicion).first()
    if not vuelo:
        db.close()
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    db.delete(vuelo)
    db.commit()
    db.close()
    return {"mensaje": f"Vuelo {vuelo.codigo} eliminado exitosamente"}

@app.patch("/vuelos/reordenar")
def reordenar_vuelos():
    db = SessionLocal()
    vuelos_reordenados = db.query(Vuelo).filter(Vuelo.estado == EstadoVuelo.RETRASADO).all()
    # Asumiendo que se desea mover los vuelos retrasados al final de la lista
    for vuelo in vuelos_reordenados:
        vuelo.estado = EstadoVuelo.PROGRAMADO  # Cambiar estado a programado para moverlos al final
        db.commit()
    db.close()
    return {"mensaje": "Vuelos reordenados exitosamente"}