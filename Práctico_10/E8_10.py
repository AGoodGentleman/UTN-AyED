import random

numeros = [random.randint(0, 100) for _ in range(6)]
array = [random.randint(0, 100) for _ in range(6)]

def selection_sort(lista):
    n = len(lista)
    for i in range(n):
        min_index = i
        #Busca el índice del elemento mínimo en el resto de la lista
        for j in range(i + 1, n):
            if lista[j] < lista[min_index]:
                min_index = j
        #Intercambia el mínimo encontrado con el primero de la parte no ordenada
        lista[i], lista[min_index] = lista[min_index], lista[i]
    return lista

def insertion_sort(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        #Mueve los elementos mayores hacia la derecha
        while j >= 0 and lista[j] > actual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista

#Lista:

print(f"Por Selection: {selection_sort(numeros)}")
print(f"Por Insertion: {insertion_sort(numeros)}")

#Array:

print(f"Por Selection: {selection_sort(array)}")
print(f"Por Insertion: {insertion_sort(array)}")