def mayor (x,y):
    if x > y:
        print("El primero es mayor al segundo.")
        return
    elif y > x:
        print("El segundo es mayor al primero.")
        return
    else:
        print("Ambos numeros son iguales.")

mayor(float(input("Ingrese un numero: ")), float(input("Ingrese otro número: ")))