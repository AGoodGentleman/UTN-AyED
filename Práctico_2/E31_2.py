pos_counter = 0

neg_counter = 0

o_counter = 0

num = int(input("Ingrese la cantidad de numeros que vaya a ingresar: "))

for i in range(num):

    j = float(input("Ingrese el siguiente numero: "))

    if j > 0:
        pos_counter +=1
    elif j < 0:
        neg_counter +=1
    else:
        o_counter += 1

print(f"La cantidad de numeros positivos fue {pos_counter}, la cantidad de numeros negativos fue {neg_counter}, la cantidad de ceros fue {o_counter}.")