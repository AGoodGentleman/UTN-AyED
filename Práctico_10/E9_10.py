import random

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

matrix = []

matrix_ordered = []

input_rows = int(input("Ingrese la cantidad de filas de su matriz: "))

input_column = int(input("Ingrese la cantidad de columnas de su matriz: "))

for row in range(input_rows): #Esto crea una matriz de 4 filas.
    rows = []
    for column in range(input_column): #Esto crea una matriz de 6 columnas.
        rows.append(random.randint(0,100))

    matrix.append(rows)

    row_ordered = insertion_sort(list(rows))

    matrix_ordered.append(row_ordered)

print(matrix)
print(matrix_ordered)