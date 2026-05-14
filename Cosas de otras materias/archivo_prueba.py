from collections import deque

# Cola: (sin deque):

cola_s = []
cola_s.append("A")
cola_s.append("B")
#print(cola_s)
#print(cola_s.pop(0))

# Pila (sin deque):

pila_s = []
pila_s.append("X")
pila_s.append("Y")
#print(pila_s)
#print(pila_s.pop())

# Cola: (con deque):

cola_c = deque()
cola_c.append("A")
cola_c.append("B")
#print(cola_c)
#print(cola_c.popleft())

# Pila: (con deque):

pila_c = deque()
pila_c.append("A")
pila_c.append("B")
#print(pila_c)
#print(pila_c.pop())

# Como deque no es mas que una clase que simboliza una cola de doble entrada o de doble extremo (doubled ended queue), podemos nosotros crearla:

class Node:
    def __init__(self,value):
        self.value = value
        self.next = None
        self.prev = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def empty(self):
        return self.head is None
    
    def add_infront(self,value):
        new = Node(value)
        if self.empty():
            self.head = self.tail = new
        
        else:
            new.next = self.head
            self.head.prev = new
            self.head = new

    def add_inback(self,value):
        new = Node(value)
        if self.empty():
            self.head = self.tail = new
        
        else:
            new.prev = self.tail
            self.tail.next = new
            self.tail = new

    def pop_infront(self):
        if self.empty():
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head:
           self.head.prev = None
        else:
            self.tail = None
        return value
    
    def pop_inback(self):
        if self.empty():
            return None
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        return value
    
    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    
print("")

dq = Deque()

dq.add_infront("a") #a
dq.add_infront("b") #ba
dq.add_infront("c") #cba
dq.add_infront("d") #dcba
dq.add_infront("e") #edcba

print(dq.to_list())

dq.add_inback(1) #edcba1
dq.add_inback(2) #edcba12
dq.add_inback(3) #edcba123
dq.add_inback(4) #edcba1234
dq.add_inback(5) #edcba12345

print(dq.to_list())

dq.pop_infront() #dcba12345

dq.pop_inback() #dcba1234

dq.pop_infront()
dq.pop_infront()
dq.pop_infront()

print(dq.to_list())

dq.pop_inback()
dq.pop_inback()
dq.pop_inback()

print(dq.to_list())

#debería quedar a1

dq.pop_infront() #1
dq.pop_infront() #
dq.pop_infront() # Aca detecta que no queda y larga none

print(dq.to_list())