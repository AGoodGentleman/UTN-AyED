import random

array = []

i = 0

while i != 20:
    array.append(random.randint(1,100))
    i += 1

print("Teniendo en cuenta que el mínimo es 1 y el máximo 20:")

X_pos = int(input("Ingrese el límite inferior: "))

Y_pos = int(input("Ingrese el límite superior: "))

print(array[X_pos:Y_pos + 1])