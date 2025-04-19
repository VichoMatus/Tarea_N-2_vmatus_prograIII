class _DoublyLinkedBase:
    """Clase base para una lista doblemente enlazada."""

    class _Node:
        """Clase para almacenar un nodo de la lista doblemente enlazada."""
        __slots__ = '_element', '_prev', '_next'  # Optimización de memoria

        def __init__(self, element, prev, next):
            self._element = element  # Referencia al elemento del vuelo
            self._prev = prev         # Referencia al nodo anterior
            self._next = next         # Referencia al nodo siguiente

    def __init__(self):
        """Crear una lista vacía con nodos centinelas."""
        self._header = self._Node(None, None, None)  # Nodo centinela
        self._trailer = self._Node(None, None, None) # Nodo centinela
        self._header._next = self._trailer  # El nodo cabecera apunta al nodo final
        self._trailer._prev = self._header  # El nodo final apunta a la cabecera
        self._size = 0  # Número de elementos

    def __len__(self):
        """Devuelve el número de elementos en la lista."""
        return self._size

    def insertar_al_frente(self, vuelo):
        """Añadir un vuelo al inicio de la lista (emergencias)."""
        new_node = self._Node(vuelo, self._header, self._header._next)
        self._header._next._prev = new_node
        self._header._next = new_node
        self._size += 1

    def insertar_al_final(self, vuelo):
        """Añadir un vuelo al final de la lista (vuelos normales)."""
        new_node = self._Node(vuelo, self._trailer._prev, self._trailer)
        self._trailer._prev._next = new_node
        self._trailer._prev = new_node
        self._size += 1

    def obtener_primer_vuelo(self):
        """Retorna el primer vuelo de la lista."""
        if self._size > 0:
            return self._header._next._element
        return None

    def obtener_ultimo_vuelo(self):
        """Retorna el último vuelo de la lista."""
        if self._size > 0:
            return self._trailer._prev._element
        return None

    def longitud(self):
        """Retorna el número total de vuelos en la lista."""
        return self._size

    def insertar_en_posicion(self, vuelo, posicion):
        """Insertar un vuelo en una posición específica."""
        current = self._header
        for _ in range(posicion):
            current = current._next
        new_node = self._Node(vuelo, current, current._next)
        current._next._prev = new_node
        current._next = new_node
        self._size += 1

    def extraer_de_posicion(self, posicion):
        """Eliminar y retornar el vuelo en una posición específica."""
        current = self._header
        for _ in range(posicion):
            current = current._next
        to_remove = current._next
        current._next = to_remove._next
        to_remove._next._prev = current
        self._size -= 1
        return to_remove._element
