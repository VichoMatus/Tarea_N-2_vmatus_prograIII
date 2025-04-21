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
def insertar_vuelo_en_posicion(codigo: str, estado: EstadoVuelo, hora: str, origen: str, destino: str, posicion: int, db: Session = Depends(get_db)):
    """
    Inserta un vuelo en una posición específica (mueve los vuelos posteriores a la derecha).
    """
    # Verificar que la posición sea válida
    if posicion < 0 or posicion > lista_vuelos.longitud():
        raise HTTPException(status_code=400, detail="Posición fuera de rango")

    # Convertimos la hora recibida a un objeto datetime
    try:
        hora_obj = datetime.strptime(hora, "%H:%M")  # El formato esperado es "HH:MM"
    except ValueError:
        raise HTTPException(status_code=400, detail="El formato de la hora no es válido. Use el formato 'HH:MM'.")

    # Crear un vuelo con los nuevos atributos
    vuelo = Vuelo(codigo=codigo, estado=estado, hora=hora_obj, origen=origen, destino=destino)
    
    # Insertar el vuelo en la posición indicada
    lista_vuelos.insertar_en_posicion(vuelo, posicion)

    # Agregar el vuelo a la base de datos
    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)

    return {"message": f"Vuelo con código {codigo} insertado en la posición {posicion}"}

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

@app.patch("/vuelos/actualizar/{codigo}")
def actualizar_estado_vuelo(codigo: str, nuevo_estado: EstadoVuelo, db: Session = Depends(get_db)):
    """
    Actualiza el estado de un vuelo y ajusta su posición en la lista.
    Si el estado cambia a 'emergencia', el vuelo se moverá al frente.
    Si el estado cambia a 'programado', el vuelo se moverá al final.
    """
    # Obtener el vuelo de la base de datos
    vuelo_db = db.query(Vuelo).filter(Vuelo.codigo == codigo).first()
    if not vuelo_db:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    
    # Obtener la posición actual del vuelo en la lista
    posicion_actual = None
    current = lista_vuelos.head
    index = 0
    while current:
        if current.data.codigo == codigo:
            posicion_actual = index
            break
        current = current.next
        index += 1

    if posicion_actual is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado en la lista")

    # Actualizar el estado del vuelo en la base de datos
    vuelo_db.estado = nuevo_estado
    db.commit()
    db.refresh(vuelo_db)

    # Reubicar el vuelo dependiendo del nuevo estado y pasar el db a mover_a_posicion
    lista_vuelos.mover_a_posicion(vuelo_db, posicion_actual, db)

    return {"message": f"Vuelo con código {codigo} actualizado a {nuevo_estado} y reposicionado en la lista."}




