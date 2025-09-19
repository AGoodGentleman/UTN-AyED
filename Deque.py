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

    def push_back(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
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

    def pop_back(self):
        if self.is_empty():
            raise IndexError("pop_back from empty deque")
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self._len -= 1
        return value

    def peek_front(self):
        if self.is_empty():
            raise IndexError("peek_front from empty deque")
        return self.head.value

    def peek_back(self):
        if self.is_empty():
            raise IndexError("peek_back from empty deque")
        return self.tail.value

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
    
dq = Deque()

dq.push_front("a")
dq.push_front("b")
dq.push_front("c")
dq.push_front("d")
dq.push_front("e")

#edcba

dq.push_back("1")
dq.push_back("2")
dq.push_back("3")
dq.push_back("4")
dq.push_back("5")

print(f"Lista inicial: {dq.to_list()}")
print(f"Longitud: {len(dq)}")
print(f"Esta vacía? {dq.is_empty()}")

#edcba12345

print(f"Peek front: {dq.peek_front()}")

# e

print(f"Peek back: {dq.peek_back()}")

# 5

dq.pop_front()

#dcba12345

dq.pop_back()

#dcba1234

print(f"Peek front tras pop: {dq.peek_front()}")

# d

print(f"Peek back tras pop: {dq.peek_back()}")

# 4

print(f"Lista: {dq.to_list()}")
print(f"Longitud: {len(dq)}")
print(f"Esta vacía? {dq.is_empty()}")

dq.pop_front()
dq.pop_front()
dq.pop_front()

dq.pop_back()
dq.pop_back()
dq.pop_back()

print(f"Lista: {dq.to_list()}")
print(f"Longitud: {len(dq)}")
print(f"Esta vacía? {dq.is_empty()}")

#a1

dq.pop_front()
#dq.pop_front()
#dq.pop_front() esta salta index error

dq.pop_back()
#dq.pop_back()
#dq.pop_back() esta salta index error

print(f"Lista final: {dq.to_list()}")
print(f"Longitud: {len(dq)}")
print(f"Esta vacía? {dq.is_empty()}")