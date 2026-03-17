matrix = []

input_rows = int(input("Ingrese la cantidad de filas de su matriz: "))

input_column = int(input("Ingrese la cantidad de columnas de su matriz: "))

for row in range(input_rows): #Esto crea una matriz de 2 filas.
    rows = []
    for column in range(input_column): #Esto crea una matriz de 3 columnas.
        rows.append(int(input("Ingrese cada numero que compone su matriz: ")))
    matrix.append(rows)
print(matrix)

print("")

i = 0
rows = len(matrix)
columns = len(matrix[i])
for row in range(rows):
    if i != len(matrix):
        for column in range(columns):
            print(matrix[row][column],end=" ")
        i += 1
        print("")

filas = len(matrix)

columnas = len(matrix[0])

print("")

print(f"La matriz tiene {filas} filas y {columnas} columnas.")

print(f"Es decir, es de {filas}x{columnas}.")