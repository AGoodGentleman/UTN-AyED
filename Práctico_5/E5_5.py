def perimeter (side):
    return side * 4

def area (side):
    return side * side

u_side = float(input("Ingrese el valor del lado de su cuadrado: "))

print(f"El perimetro de su cuadrado es {perimeter(u_side)}.")

print(f"El area de su cuadrado es {area(u_side)}.")