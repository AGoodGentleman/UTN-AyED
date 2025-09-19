class stack():
    def __init__(self):
        self.item = []

    def empty(self):
        if len(self.item) == 0:
            return True
        else: 
            return False
        
    def eliminar(self):
        if self.empty():
            raise IndexError("Lista vacia")
        else:
            self.item.pop()
        
    def add(self,value):
        self.item.append(value)

    def mirar(self):
        if self.empty():
            raise IndexError("Lista vacia")
        else:
            return self.item[-1]
        
    def to_list(self):
        for item in self.item:
            print(item, "", end=" ")

pile = stack()

print(pile.empty())

print("")

pile.add(1)
pile.add(2)
pile.add(3)
pile.add(4)
pile.add(5)

print(pile.mirar())

pile.to_list()

print("")
print("")

pile.eliminar()

print(pile.mirar())

pile.to_list()