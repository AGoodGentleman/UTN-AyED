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
        
contenedores = Pila()
contenedores_new = Pila()
objective = Pila()

cantidad = int(input("Ingrese el numero de contenedores que tenga: "))

i = 1

while i <= cantidad:
    contenedores.push(f"Contenedor n° {i} ") 
    i += 1

print(contenedores.value)

extract = 0

extract = int(input("Ingrese qué contenedor quiere retirar: ")) + 1

difference = cantidad - extract + 1

i = 0

if extract <= cantidad:
    while i < cantidad:
        contenedores_new.value.append(contenedores.value[0])
        contenedores.pop()
        i += 1
        if i == difference:
            objective.push(contenedores.value[0])
            contenedores.pop()
            i += 1

print(contenedores_new.value)
print(objective.value)