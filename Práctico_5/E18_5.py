def rectangle(char, side):
    if side < 2:
        print("El lado debe ser al menos 2 para formar un rectangulo hueco.")
        return

    print(char * side)

    for i in range(side - 2):
        print(char + " " * (side - 2) + char)

    print(char * side)

rectangle(str(input("Ingrese su caracter: ")), int(input("Ingrese la anchura de su rectangulo: ")))