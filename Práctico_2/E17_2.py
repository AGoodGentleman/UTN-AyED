m1 = input("Ingrese la primer película: ")
m2 = input("Ingrese la segunda película: ")
m3 = input("Ingrese la tercer película: ")
m4 = input("Ingrese la cuarta película: ")
m5 = input("Ingrese la quinta película: ")
m6 = input("Ingrese la sexta película: ")
m7 = input("Ingrese la séptima película: ")
m8 = input("Ingrese la octava película: ")
m9 = input("Ingrese la novena película: ")
m10 = input("Ingrese la última película: ")

my_list = [m1, m2, m3, m4, m5, m6, m7, m8, m9, m10]

n = 0

n = int(input("Ingrese un numero entero del 1 al 10: "))

if n < 1 or n > 10:
    print ("No existe una película en ese lugar")
else:
    print ("La película en ese lugar de la lista es: ")
    print (my_list[n-1])