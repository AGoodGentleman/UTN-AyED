numerator = float(input("Ingrese un numerador: "))
denominator = float(input("Ingrese un denominador o divisor: "))
if denominator == 0:
    print("El denominador o divisor será cero, por lo cual la división no podrá llevarse a cabo.")
else:
    print("La division entre dichos numeros es {0}".format(numerator/denominator))