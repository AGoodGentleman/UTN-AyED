q_grades = int(input("Ingrese la cantidad de notas que desee guardar: "))

grade_list = []

for i in range(q_grades):
    grade = float(input("Ingrese su nota: "))
    grade_list.append(grade)

print("Sus notas guardadas son: ")

for element in grade_list:
    print(element)