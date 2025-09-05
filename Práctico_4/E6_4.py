import random

array = []

i = 0

while i != 30:
    array.append(random.randint(1,100))
    i += 1

X_pos = int(input("Ingrese una posición entre 1 y 30: ")) - 1

Y_pos = int(input("Ingrese otra posición entre 1 y 30: ")) - 1

print(f"El vector original era {array}.")

Y = array[X_pos]

X = array[Y_pos]

array[X_pos] = X

array[Y_pos] = Y

print(f"El vector con posiciones X e Y cambiadas es {array}.")