import random

matrix_A = []
matrix_B = []
matrix_C = [0,0,0]

for row in range(4):  # 4 filas
    rows = []
    row_sum = 0
    for column in range(3):  # 3 columnas
        num = random.randint(0, 9)
        rows.append(num)
        row_sum += num
        matrix_C[column] += num
    matrix_A.append(rows)
    matrix_B.append(row_sum)

print("Matriz A:")
for element in matrix_A:
    print(element)

print(f"Suma de filas (matriz B): {matrix_B}.")
print(f"Suma de columnas (matriz C): {matrix_C}.")