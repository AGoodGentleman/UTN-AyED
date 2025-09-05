def mult (num, line):
    return num * line

num = int(input("Ingrese un numero entero: "))

for i in range (10):
    print(f"Su numero multiplicado por {i+1} es igual a {mult(num,i+1)}.")