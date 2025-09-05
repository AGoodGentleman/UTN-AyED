import random

array = []

i = 0

sum = 0

average = 0

while i != 18:
    array.append(random.randint(1,50))
    i += 1

for element in array:
    sum = sum + element

average = sum/18

print(f"El vector era {array}.")

print(f"El promedio de sus elementos es {average}.")