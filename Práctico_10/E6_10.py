import array

import random

def insertion_sort_array(arr):
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        # Mueve los elementos mayores hacia la derecha
        while j >= 0 and arr[j] > actual:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual
    return arr

def selection_sort_array(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        # Busca el índice del elemento mínimo en el resto del array
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # Intercambia el mínimo encontrado con el primero de la parte no ordenada
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def bubble_sort_array(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                # Intercambia si están en orden incorrecto
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

arr = array.array("i",[random.randint(0,100) for _ in range(10)])

print(f"Insertion sort: {insertion_sort_array(arr)}")
print(f"Selection sort: {selection_sort_array(arr)}")
print(f"Bubble sort: {bubble_sort_array(arr)}")