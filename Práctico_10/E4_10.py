import random

def quick_sort(lista):
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]
    return quick_sort(menores) + iguales + quick_sort(mayores)

file_name = "nros.txt"
with open(file_name, "w") as file:
    for _ in range(50):
        numero = random.randint(0, 100)
        file.write(f"{numero}\n")

with open(file_name, "r") as file:
    num_list = [int(line.strip()) for line in file.readlines()]

print("Lista original:")
print(num_list)

ordenada = quick_sort(num_list)

print("\nLista ordenada:")
print(ordenada)

with open("ordenado.txt", "w") as file:
    for n in ordenada:
        file.write(f"{n}\n")