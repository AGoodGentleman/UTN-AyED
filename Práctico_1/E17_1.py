print("Este programa se ejecuta con la asuncion de que el usuario quiere ordenar en forma creciente tres numeros distintos entre si.")
num1 = float(input("Ingrese un numero: "))
num2 = float(input("Ingrese otro numero: "))
num3 = float(input("Ingrese otro numero: "))
if num1 > num2 and num1 > num3:
    if num2 > num3:
        print(f"{num3}, {num2}, {num1}")
    elif num3 > num2:
        print(f"{num2}, {num3}, {num1}")
elif num2 > num1 and num2 > num3:
    if num1 > num3:
         print(f"{num3}, {num1}, {num2}")
    elif num3 > num1:
        print(f"{num1}, {num3}, {num2}")
elif num3 > num1 and num3 > num2:
    if num1 > num2:
         print(f"{num2}, {num1}, {num3}")
    elif num2 > num1:
        print(f"{num1}, {num2}, {num3}")