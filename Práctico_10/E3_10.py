def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                #Intercambia si están en orden incorrecto
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

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

num_list = []
i = 0

while i < 6:
    num_list.append(int(input("Ingrese el próximo número entero: ")))
    i += 1

print(f"Bubble sort: {bubble_sort(num_list)}")
print(f"Selection sort: {selection_sort(num_list)}")
print(f"Insertion sort: {insertion_sort(num_list)}")