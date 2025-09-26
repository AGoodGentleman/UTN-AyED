class Node:
    "Nodo de una lista simplemente enlazada."
    __slots__ = ("data", "next")
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    "Lista simplemente enlazada."
    def __init__(self, iterable=None):
        self.head = None
        self._size = 0
        if iterable:
            for x in iterable:
                self.push_back(x)

    # --- consultas básicas ---
    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def __iter__(self):
        curr = self.head
        while curr:
            yield curr.data
            curr = curr.next

    # --- inserciones ---
    def push_front(self, value):
        "Inserta al inicio"
        self.head = Node(value, self.head)
        self._size += 1

    def push_back(self, value):
        "Inserta al final"
        new_node = Node(value)
        if not self.head:
            self.head = new_node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new_node
        self._size += 1

    def insert(self, index, value):
        "Inserta en posición/índice."
        if index < 0 or index > self._size:
            raise IndexError("índice fuera de rango")
        if index == 0:
            return self.push_front(value)
        prev = self._node_at(index - 1)
        prev.next = Node(value, prev.next)
        self._size += 1

    # --- eliminaciones ---
    def pop_front(self):
        "Elimina y devuelve el primero."
        if not self.head:
            raise IndexError("lista vacía")
        value = self.head.data
        self.head = self.head.next
        self._size -= 1
        return value

    def pop_back(self):
        "Elimina y devuelve el último."
        if not self.head:
            raise IndexError("lista vacía")
        if not self.head.next:
            return self.pop_front()
        prev = self.head
        curr = self.head.next
        while curr.next:
            prev, curr = curr, curr.next
        prev.next = None
        self._size -= 1
        return curr.data

    def remove(self, value):
        "Elimina la primera ocurrencia de value. Devuelve True si eliminó."
        if not self.head:
            return False
        if self.head.data == value:
            self.head = self.head.next
            self._size -= 1
            return True
        prev = self.head
        curr = self.head.next
        while curr:
            if curr.data == value:
                prev.next = curr.next
                self._size -= 1
                return True
            prev, curr = curr, curr.next
        return False

    # --- búsqueda ---
    def find(self, value):
        "Devuelve el índice de la primera ocurrencia o -1 si no está."
        idx = 0
        curr = self.head
        while curr:
            if curr.data == value:
                return idx
            curr = curr.next
            idx += 1
        return -1

    # --- utilidades privadas ---
    def _node_at(self, index):
        "Devuelve el nodo en posición index."
        if index < 0 or index >= self._size:
            raise IndexError("índice fuera de rango")
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr

ll = LinkedList([10, 20, 30])
ll.push_front(5)        # [5, 10, 20, 30]
ll.push_back(40)        # [5, 10, 20, 30, 40]
ll.insert(2, 15)        # [5, 10, 15, 20, 30, 40]
ll.remove(20)           # [5, 10, 15, 30, 40]
print(ll, "len=", len(ll))
print("índice de 30:", ll.find(30))