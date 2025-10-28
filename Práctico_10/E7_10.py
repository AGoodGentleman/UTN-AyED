price_list = []

i = 0

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

while i < 10:
    price_list.append(float(input("Ingrese el precio de la próxima golosina: ")))
    i += 1

print(f"Lista ordenada por Selection: {selection_sort(price_list)}")
print(f"Lista ordenada por Insertion: {insertion_sort(price_list)}")