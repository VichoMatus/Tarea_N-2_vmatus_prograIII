class DoublyLinkedList:
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insertar_al_frente(self, vuelo):
        new_node = self.Node(vuelo)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
        print(f"Vuelo agregado al frente: {vuelo.codigo}")  # Verificar que el vuelo se agregue
    
    def insertar_al_final(self, vuelo):
        new_node = self.Node(vuelo)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        print(f"Vuelo agregado al final: {vuelo.codigo}")  # Verificar que el vuelo se agregue


    def obtener_primero(self):
        # Retornar (sin remover) el primer vuelo de la lista
        if self.head:
            return self.head.data
        return None

    def obtener_ultimo(self):
        # Retornar (sin remover) el último vuelo de la lista
        if self.tail:
            return self.tail.data
        return None

    def longitud(self):
        # Retorna el número total de vuelos en la lista
        return self.size

    def extraer_de_posicion(self, posicion):
        """
        Remueve y retorna el vuelo en la posición dada (ej: cancelación).
        """
        if posicion < 0 or posicion >= self.size:
            raise IndexError("Índice fuera de rango")
        
        current = self.head
        for _ in range(posicion):
            current = current.next
        
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
        if current == self.head:
            self.head = current.next
        if current == self.tail:
            self.tail = current.prev
        self.size -= 1
        return current.data


    def extraer_de_posicion(self, posicion):
        """
        Remueve y retorna el vuelo en la posición dada (ej: cancelación).
        """
        if posicion < 0 or posicion >= self.size:
            raise IndexError("Índice fuera de rango")
        
        current = self.head
        for _ in range(posicion):
            current = current.next
        
        # Conectar los nodos alrededor del nodo a eliminar
        if current.prev:
            current.prev.next = current.next
        if current.next:
            current.next.prev = current.prev
        if current == self.head:  # Si es el primer nodo
            self.head = current.next
        if current == self.tail:  # Si es el último nodo
            self.tail = current.prev
        
        self.size -= 1
        return current.data  # Retornar el vuelo eliminado
