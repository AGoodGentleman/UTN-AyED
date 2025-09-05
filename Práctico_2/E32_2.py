option = input("Si desea iniciar, escriba cualquier valor. Si desea salir, escriba 's': ")

num_list = []

while option != "s":
    number = float(input("Ingrese su siguiente numero: "))
    num_list.append(number)
    option = input("Si desea iniciar, escriba cualquier letra. Si desea salir, escriba 's': ")

print("Usted ha ingresado: ")

for element in num_list:
    print(element)