matrix_multi = [[[1,2,3],[3,4,5],[5,6,7]],
                [[7,8,9],[9,1,2],[2,3,4]],
                [[4,5,6],[6,7,8],[8,9,1]]]

print(matrix_multi)

profundidad = len(matrix_multi)

filas = len(matrix_multi[0])

columnas = len(matrix_multi[0][0])

print(f"La matriz tiene {profundidad} de profundidad, {filas} filas y {columnas} columnas.")

print(f"Es decir, es de {filas}x{columnas}x{profundidad}.")