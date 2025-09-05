import random

matrix = []

for row in range(4): #Esto crea una matriz de 4 filas.
    rows = []
    for column in range(3): #Esto crea una matriz de 3 columnas.
        rows.append(random.randint(0,9))
    matrix.append(rows)
print(matrix)