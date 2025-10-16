#Bubble Sort

def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                #Intercambia si están en orden incorrecto
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

#Ejemplo

numeros_1 = [7, 2, 9, 4, 1, 10, 3, 6, 8, 5]
print(bubble_sort(numeros_1))

#Selection Sort

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

#Ejemplo

numeros_2 = [7, 2, 9, 4, 1, 10, 3, 6, 8, 5]
print(selection_sort(numeros_2))

#Insertion Sort

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

#Ejemplo

numeros_3 = [7, 2, 9, 4, 1, 10, 3, 6, 8, 5]
print(insertion_sort(numeros_3))

#Merge Sort

def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])

    return merge(izquierda, derecha)

def merge(izquierda, derecha):
    resultado = []
    i = j = 0

    #Mezcla las dos mitades ordenadas
    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    #Agrega los elementos restantes
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

#Ejemplo

numeros_4 = [7, 2, 9, 4, 1, 10, 3, 6, 8, 5]
print(merge_sort(numeros_4))

#Quick Sort

def quick_sort(lista):
    #Si la lista tiene 0 o 1 elemento, ya está ordenada
    if len(lista) <= 1:
        return lista

    #Elegimos un pivote (en este caso, el elemento del medio)
    pivote = lista[len(lista) // 2]

    #Particionamos la lista en tres partes:
    menores = [x for x in lista if x < pivote]
    iguales = [x for x in lista if x == pivote]
    mayores = [x for x in lista if x > pivote]

    #Ordenamos recursivamente las sublistas y las concatenamos
    return quick_sort(menores) + iguales + quick_sort(mayores)

#Ejemplo

numeros_5 = [8, 3, 1, 7, 0, 10, 2]
ordenados = quick_sort(numeros_5)
print("Lista original:", numeros_5)
print("Lista ordenada:", ordenados)
