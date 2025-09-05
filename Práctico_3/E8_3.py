ages = {"Juan": 30, "María": 25, "Pedro": 35}

ages["Ana"] = 28

for element in ages:
    print(element)
    print(ages[element])

print("")

name = input("Ingrese un nombre para verificar su existencia en el diccionario: ")

for element in ages:
    if element == name:
        print(f"La persona llamada {name} se encuentra en el diccionario.")
        break
else:
    print(f"La persona llamada {name} NO se encuentra en el diccionario.")