import random

array = []

i = 0

min = 51

max = 0

while i != 18:
    array.append(random.randint(1,50))
    i += 1

print(f"El vector era {array}.")

for element in array:
    if element >= max:
        max = element
    elif element <= min:
        min = element

print(f"El mínimo del vector es {min} y el máximo es {max}.")