ran = int(input("Ingrese un numero mayor a 1 y menor a 50: "))

if ran > 1 and ran < 50:
    for i in range(1, ran + 1):
        print(i)
else:
    print("El numero no cumple con los parametros establecidos.")