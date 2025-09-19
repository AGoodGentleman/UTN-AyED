class Pila:
    def __init__(self):
        self.value = []
    def push(self, element):
        self.value.append(element)
    def pop(self):
        self.value.pop(0)
    def __str__(self):
        chain = ""
        for element in self.value:
            chain += element
        return chain
    def empty(self):
        if len(self.value) == 0:
            return True
        else:
            return False


pile = Pila()

cadena = input("Ingrese su cadena de texto: ")

balanced = True

for element in cadena:
    if element == "(":
        pile.push(element)
    if element == ")":
        if pile.empty():
            balanced = False
            break
        else:
            pile.pop()

if pile.empty() and balanced == True:
    print("Balanceado")
else:
    print("No Balanceado")