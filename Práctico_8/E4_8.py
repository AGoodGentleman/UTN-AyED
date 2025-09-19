dq_inv = []

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None
        self._len = 0

    def __len__(self):
        return self._len

    def is_empty(self):
        return self._len == 0

    def push_front(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._len += 1

    def pop_front(self):
        if self.is_empty():
            raise IndexError("pop_front from empty deque")
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._len -= 1
        return value

    def peek_front(self):
        if self.is_empty():
            raise IndexError("peek_front from empty deque")
        return self.head.value

    def to_list(self):
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.value
            cur = cur.next

    def clear(self):
        self.head = self.tail = None
        self._len = 0

    def __repr__(self):
        return f"Deque({self.to_list()})"
    
    def InvertirPila(self):
        global dq_inv
        out = []
        cur = self.tail
        while cur:
            out.append(cur.value)
            cur = cur.prev
        dq_inv = out
        return out
    
dq = Deque()

keep_going = True
letter = ""

while keep_going:
    letter = input("Ingrese el próximo pueblo, si desea parar, ingrese 0: ")
    if letter == "0":
        keep_going = False
    else:    
        dq.push_front(letter)

print(f"De ida: {dq.InvertirPila()}")

print(f"De vuelta: {dq.to_list()}")