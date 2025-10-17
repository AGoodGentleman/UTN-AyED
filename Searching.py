#Interpolation Search

def interpolation_search(lista_ordenada, objetivo):
    low = 0
    high = len(lista_ordenada) - 1

    while low <= high and lista_ordenada[low] <= objetivo <= lista_ordenada[high]:
        if lista_ordenada[high] == lista_ordenada[low]:
            return low if lista_ordenada[low] == objetivo else -1

        pos = low + int(
            ( (objetivo - lista_ordenada[low]) * (high - low) ) /
            (lista_ordenada[high] - lista_ordenada[low])
        )

        if pos < low or pos > high:
            return -1

        if lista_ordenada[pos] == objetivo:
            return pos
        elif lista_ordenada[pos] < objetivo:
            low = pos + 1
        else:
            high = pos - 1

    return -1


#Ejemplo

nums_ordenados = list(range(0, 101, 5))   # [0, 5, 10, ..., 100]
print("Lista:", nums_ordenados)

for x in [0, 35, 90, 101]:
    idx = interpolation_search(nums_ordenados, x)
    if idx != -1:
        print(f"Encontré {x} en índice {idx}")
    else:
        print(f"{x} no está en la lista")

#Linear Search

def linear_search(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1

#Ejemplo

numeros_1 = [7, 2, 9, 4, 1, 10, 3, 6, 8, 5]
print("Lista:", numeros_1)

valor = 4
indice = linear_search(numeros_1, valor)
if indice != -1:
    print(f"Encontré {valor} en la posición {indice}")
else:
    print(f"{valor} no está en la lista")

#Binary Search

def binary_search(lista_ordenada, objetivo):
    low = 0
    high = len(lista_ordenada) - 1

    while low <= high:
        mid = (low + high) // 2  #Punto medio

        if lista_ordenada[mid] == objetivo:
            return mid
        elif lista_ordenada[mid] < objetivo:
            low = mid + 1
        else:
            high = mid - 1

    return -1

#Ejemplo

numeros_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("Lista ordenada:", numeros_2)

valor = 7
indice = binary_search(numeros_2, valor)
if indice != -1:
    print(f"Encontré {valor} en la posición {indice}")
else:
    print(f"{valor} no está en la lista")