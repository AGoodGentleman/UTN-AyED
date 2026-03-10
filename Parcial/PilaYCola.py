# --- Pila ---

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack vacío")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack vacío")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

# --- Cola ---

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue vacía")
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("Queue vacía")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)