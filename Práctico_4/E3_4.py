import random

i = 0

array = []

while i != 20:
    array.append(random.randint(5,30))
    i += 1

option = int(input("Ingrese un valor entre 5 y 30: "))

for element in array:
    if option == element:
        print(f"El numero {option} pertenece al vector.")
        break
else:
    print(f"El numero {option} NO pertenece al vector.")