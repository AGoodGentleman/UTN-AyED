import random

array = []

new_array = []

i = 0

ocupada_c = 0

libre_c = 0

butaca_c = int(input("Ingrese la cantidad de butacas de su cine ficticio: "))

while i != butaca_c:
    butaca = random.randint(0,1)
    if butaca == 0:
        array.append(False)
    elif butaca == 1:
        array.append(True)
    i += 1

for element in array:
    if element == True:
        new_array.append("Ocupada")
        ocupada_c += 1
    elif element == False:
        new_array.append("Libre")
        libre_c += 1

print("Su cine se vería así:")

print(new_array)

print(f"Con {ocupada_c} butacas ocupadas y {libre_c} butacas libres.")