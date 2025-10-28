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

num_list = [6, 2, 4, 8, 3, 7, 5]