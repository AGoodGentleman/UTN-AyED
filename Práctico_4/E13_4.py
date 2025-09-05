import random

matrix = []

i = 1

j = 1

col_elem = []

for row in range(5): #Esto crea una matriz de 5 filas.
    rows = []
    
    for column in range(4): #Esto crea una matriz de 4 columnas.
        rows.append(random.randint(0,9))
    matrix.append(rows)
    print (f"La fila {i} es {rows}.")
    i += 1

i = 1

j = 0

for j in range(4):
    col_elem = []
    
    for i in range(5):
        col_elem.append(matrix[i][j])
    
    print(f"La columna {j + 1} es {col_elem}")