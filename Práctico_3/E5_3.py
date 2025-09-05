name = input("Ingrese su nombre: ")

print(f"Bienvenido {name}.")

print("Para ingresar notas, escriba 1.")

print("Para salir, escriba 0.")

option = int(input(""))

student = ""

grade = 0

dictionary = {}

if option != 0:
    while option != 0:
        student = input("Ingrese el nombre del estudiante: ")
        grade = float(input("Ingrese la nota del estudiante: "))
        dictionary[student] = grade
        option = int(input("1 para seguir, 0 para salir: "))
        if option == 1:
            pass
        elif option == 0:
            break

    option_1 = int(input("Si desea chequear las notas de los estudiantes, ingrese 1. De lo contrario, ingrese 0: "))

    while option_1 != 0:
        student = input("Ingrese el nombre del estudiante del que quiera ver su nota: ")
        print(f"{student} obtuvo un {dictionary[student]}.")
        option_1 = int(input("Para seguir, ingrese 1, para salir, ingrese 0: "))
        if option_1 == 1:
            pass
        elif option_1 == 0:
            break

print(f"Muchas gracias {name}, vuelva pronto.")