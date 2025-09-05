array = []

option = ""

while option != "zzz":
    option = input("Ingrese el nombre a cargar en el vector. Ingrese zzz para terminar: ")
    array.append(option)
    
array.remove("zzz")

print(array)