class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class Linked_List:
    def __init__(self):
        self.head = None
        self._size = 0

    def push_front(self, value):
        self.head = Node(value, self.head)
        self._size += 1

    def push_back(self,value):
        if not self.head:
            self.head = Node(value)
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = Node(value)
        self._size += 1

    def pop_front(self):
        if not self.head:
            raise IndexError("lista vacía")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        print(value)
        
    def pop_back(self):
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
        print(curr.value)

    def to_list(self):
        out = []
        curr = self.head
        while curr:
            out.append(curr.value)
            curr = curr.next
        return out
    
ll = Linked_List()

print(ll.to_list())
ll.push_front(1)
print(ll.to_list())
ll.push_back(2)
print(ll.to_list())
ll.pop_front()
ll.pop_back()
print(ll.to_list())
