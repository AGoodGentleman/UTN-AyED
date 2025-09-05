import random

matrix = []

sum_row = 0

sum_col = 0

for row in range(4): #Esto crea una matriz de 4 filas.
    rows = []
    for column in range(3): #Esto crea una matriz de 3 columnas.
        rows.append(random.randint(0,9))
    matrix.append(rows)
    
    for element in rows:
        sum_row = sum_row + element

i = 1

j = 0

for j in range(3):
    col_elem = []
    
    for i in range(4):
        col_elem.append(matrix[i][j])
    
    for element in col_elem:
        sum_col = sum_col + element

print(matrix)

print(f"La suma de las columnas es {sum_col}.")

print(f"La suma de las filas es {sum_row}.")