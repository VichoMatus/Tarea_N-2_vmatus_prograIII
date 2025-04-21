from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Vuelo, EstadoVuelo
from database import get_db
from doubly_linked_list import DoublyLinkedList  # Importamos la clase DoublyLinkedList
from datetime import datetime
app = FastAPI()

# Instanciamos la lista doblemente enlazada
lista_vuelos = DoublyLinkedList()

@app.on_event("startup")
def cargar_vuelos_iniciales():
    """
    Carga los vuelos de la base de datos en la lista enlazada al iniciar la aplicación.
    """
    # Utiliza el get_db para obtener la sesión de base de datos
    db = next(get_db())  # Esto obtiene la sesión de la base de datos
    vuelos_db = db.query(Vuelo).all()  # Recupera todos los vuelos desde la base de datos
    
    for vuelo in vuelos_db:
        # Dependiendo del estado del vuelo, inserta en la lista
        if vuelo.estado == EstadoVuelo.emergencia:
            lista_vuelos.insertar_al_frente(vuelo)
        else:
            lista_vuelos.insertar_al_final(vuelo)
    
    print("Vuelos cargados desde la base de datos en la lista enlazada.")




@app.post("/vuelos/")
def crear_vuelo(codigo: str, estado: EstadoVuelo, hora: str, origen: str, destino: str, db: Session = Depends(get_db)):
    """
    Crea un vuelo y lo agrega al final o al frente dependiendo del estado.
    Si el estado es 'emergencia', el vuelo se agrega al frente.
    """
    # Verificar si ya existe un vuelo con el mismo código
    vuelo_existente = db.query(Vuelo).filter(Vuelo.codigo == codigo).first()
    if vuelo_existente:
        raise HTTPException(status_code=400, detail="Ya existe un vuelo con este código.")
    
    try:
        # Convertimos la hora recibida a un objeto datetime
        hora_obj = datetime.strptime(hora, "%H:%M")  # El formato esperado es "HH:MM"
    except ValueError:
        raise HTTPException(status_code=400, detail="El formato de la hora no es válido. Use el formato 'HH:MM'.")

    # Crear un vuelo con los nuevos atributos
    vuelo = Vuelo(codigo=codigo, estado=estado, hora=hora_obj, origen=origen, destino=destino)
    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)
    
    # Si el estado es 'emergencia', insertar al frente
    if estado == EstadoVuelo.emergencia:
        lista_vuelos.insertar_al_frente(vuelo)
    else:
        lista_vuelos.insertar_al_final(vuelo)
    
    return vuelo


@app.get("/vuelos/lista")
def obtener_lista_vuelos():
    """
    Lista todos los vuelos en orden actual desde la lista enlazada.
    """
    vuelos = []
    current = lista_vuelos.head
    while current:
        vuelos.append(current.data)
        current = current.next
    return vuelos



@app.get("/vuelos/proximo")
def obtener_proximo_vuelo():
    """
    Retorna el primer vuelo sin remover.
    """
    vuelo = lista_vuelos.obtener_primero()
    if vuelo:
        return vuelo
    return {"message": "No hay vuelos en la lista"}

@app.get("/vuelos/ultimo")
def obtener_ultimo_vuelo():
    """
    Retorna el último vuelo sin remover.
    """
    vuelo = lista_vuelos.obtener_ultimo()
    if vuelo:
        return vuelo
    return {"message": "No hay vuelos en la lista"}

@app.post("/vuelos/inserta")
def insertar_vuelo_en_posicion(vuelo_id: int, posicion: int, db: Session = Depends(get_db)):
    """
    Inserta un vuelo en una posición específica.
    """
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    
    lista_vuelos.insertar_en_posicion(vuelo, posicion)
    return {"message": "Vuelo insertado en la posición deseada"}

@app.delete("/vuelos/extrair")
def eliminar_vuelo_en_posicion(posicion: int, db: Session = Depends(get_db)):
    """
    Remueve un vuelo en la posición dada en la lista doblemente enlazada y lo elimina de la base de datos.
    """
    if posicion < 0 or posicion >= lista_vuelos.longitud():
        raise HTTPException(status_code=400, detail="Posición inválida o fuera de rango")

    # Extraer el vuelo de la lista (por posición)
    vuelo = lista_vuelos.extraer_de_posicion(posicion)

    # Eliminar el vuelo de la base de datos
    vuelo_db = db.query(Vuelo).filter(Vuelo.codigo == vuelo.codigo).first()
    if vuelo_db:
        db.delete(vuelo_db)
        db.commit()

    return {"message": f"Vuelo con código {vuelo.codigo} eliminado de la posición {posicion}"}




@app.get("/vuelos/lista")
def obtener_lista_vuelos():
    """
    Lista todos los vuelos en orden actual.
    """
    vuelos = []
    current = lista_vuelos.head
    while current:
        vuelos.append(current.data)
        current = current.next
    return vuelos

@app.patch("/vuelos/reordenar")
def reordenar_vuelos(db: Session = Depends(get_db)):
    """
    Reordena los vuelos por algún criterio (por ejemplo, por retrasos).
    """
    vuelos = db.query(Vuelo).all()
    vuelos_ordenados = sorted(vuelos, key=lambda x: x.estado == EstadoVuelo.emergencia, reverse=True)  # Emergencias primero
    return {"message": "Cola reordenada", "vuelos": vuelos_ordenados}
