file_name = "pacientes.txt"

file = open(file_name, "w")

def insertion_sort(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and lista[j][2] > actual[2]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista

file.write("Sanchez\n")
file.write("Luis\n")
file.write("64\n")
file.write("OSDE\n")
file.write("Balaz\n")
file.write("Sara\n")
file.write("32\n")
file.write("OSECAD\n")
file.write("Lipa\n")
file.write("Julieta\n")
file.write("27\n")
file.write("OSDE\n")
file.write("Perez\n")
file.write("Lucila\n")
file.write("30\n")
file.write("OSECAD\n")
file.close()

with open(file_name, "r") as file:
    lineas = [line.strip() for line in file]

pacientes = []
for i in range(0, len(lineas), 4):
    apellido = lineas[i]
    nombre = lineas[i + 1]
    edad = int(lineas[i + 2])
    obra_social = lineas[i + 3]
    pacientes.append((apellido, nombre, edad, obra_social))

pacientes_ordenados = insertion_sort(pacientes.copy())

file_name = "Pacientes_Ordenados.txt"
with open(file_name, "w") as file:
    for p in pacientes_ordenados:
        file.write(f"{p[0]}\n{p[1]}\n{p[2]}\n{p[3]}\n")

with open(file_name, "r") as file:
    print(file.read())
