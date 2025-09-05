my_list = []

grade = 0

for i in range(8):
    grade = float(input("Ingrese sus notas: "))
    my_list.append(grade)

Promedio = sum(my_list)/8

print(f"Su promedio es {round(Promedio,2)}")