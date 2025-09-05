import random

matrix = []

for row in range(5): #Esto crea una matriz de 5 filas.
    rows = []
    for column in range(6): #Esto crea una matriz de 6 columnas.
        rows.append(random.randint(1,6))
    matrix.append(rows)
print(matrix)

matrix[4] = [0,0,0,0,0,0]

print (matrix)