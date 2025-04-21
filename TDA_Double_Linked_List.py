from models import EstadoVuelo  # Asegúrate de importar la clase EstadoVuelo


class DoublyLinkedList:
    class Node:
        def __init__(self, data=None):
            self.data = data
            self.prev = None
            self.next = None

    def __init__(self):
        """Crear una lista vacía con nodos centinelas."""
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        """Devuelve el número de elementos en la lista."""
        return self.size

    def insertar_al_frente(self, vuelo):
        """Añadir un vuelo al inicio de la lista (emergencias)."""
        new_node = self.Node(vuelo)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
        print(f"Vuelo agregado al frente: {vuelo.codigo}")

    def insertar_al_final(self, vuelo):
        """Añadir un vuelo al final de la lista (vuelos normales)."""
        new_node = self.Node(vuelo)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
        print(f"Vuelo agregado al final: {vuelo.codigo}")

    def obtener_primero(self):
        """Retorna el primer vuelo de la lista (sin removerlo)."""
        if self.head:
            return self.head.data
        return None

    def obtener_ultimo(self):
        """Retorna el último vuelo de la lista (sin removerlo)."""
        if self.tail:
            return self.tail.data
        return None

    def longitud(self):
        """Retorna el número total de vuelos en la lista."""
        return self.size

    def extraer_de_posicion(self, posicion):
        """Eliminar y retornar el vuelo en una posición específica."""
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

    def insertar_en_posicion(self, vuelo, posicion):
        """Inserta un vuelo en una posición específica (ej: índice 2)."""
        if posicion < 0 or posicion > self.size:
            raise IndexError("Índice fuera de rango")

        new_node = self.Node(vuelo)

        # Si la posición es 0, inserta al frente
        if posicion == 0:
            self.insertar_al_frente(vuelo)
        # Si la posición es igual al tamaño, inserta al final
        elif posicion == self.size:
            self.insertar_al_final(vuelo)
        else:
            # Si la posición es intermedia
            current = self.head
            for _ in range(posicion):
                current = current.next

            # Insertamos el nuevo nodo en la posición deseada
            new_node.next = current
            new_node.prev = current.prev
            current.prev.next = new_node
            current.prev = new_node

            self.size += 1

    def mover_a_posicion(self, vuelo, nueva_posicion):
        """
        Mueve un vuelo a una nueva posición en la lista.
        Si el vuelo está en la lista, lo elimina de su posición actual
        y lo inserta en la nueva posición.
        """
        # Buscar el vuelo por su código en la lista
        current = self.head
        posicion_actual = None
        index = 0
        while current:
            if current.data.codigo == vuelo.codigo:  # Usamos el código para comparar
                posicion_actual = index
                break
            current = current.next
            index += 1

        if posicion_actual is None:
            raise ValueError("El vuelo no se encuentra en la lista.")

        # Eliminar el vuelo de su posición actual
        self.extraer_de_posicion(posicion_actual)

        # Si el vuelo cambia a emergencia, insertarlo al frente
        if vuelo.estado == EstadoVuelo.emergencia:
            self.insertar_al_frente(vuelo)
        # Si el vuelo cambia a programado, insertarlo al final (o en su posición original)
        elif vuelo.estado == EstadoVuelo.programado:
            self.insertar_al_final(vuelo)
