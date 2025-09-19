class Pila:
    def __init__(self):
        self.value = []
    def push(self, element):
        self.value.insert(0, element)
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
        
inv_word = Pila()

add = ""

word = input("Ingrese su cadena de texto: ")

for char in word:
    if char != " ":
        add += char
    else:
        inv_word.push(add)
        add = ""
        inv_word.push(" ")
inv_word.push(add)

print(word)

print(inv_word)