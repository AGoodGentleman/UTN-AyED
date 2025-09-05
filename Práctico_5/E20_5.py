list_a = []
list_b = []
list_c = []
option = ""

while option != "Parar":
    option = input("Ingrese el número a añadir a Lista A, recuerde ingresar Parar para parar: ")
    if option != "Parar":
        list_a.append(int(option))

option = ""

while option != "Parar":
    option = input("Ingrese el número a añadir a Lista B, recuerde ingresar Parar para parar: ")
    if option != "Parar":
        list_b.append(int(option))

def search(list_a, list_b, check):
    list_c = []

    if check:
        for element_a in list_a:
            if element_a in list_b and element_a not in list_c:
                list_c.append(element_a)
    else:
        for element_a in list_a:
            if element_a not in list_b and element_a not in list_c:
                list_c.append(element_a)
        for element_b in list_b:
            if element_b not in list_a and element_b not in list_c:
                list_c.append(element_b)
                
    return list_c

entrada_check = input("Ingrese True o False: ")
if entrada_check == "True":
    check = True
else:
    check = False

print("Resultado en lista C:", search(list_a, list_b, check))