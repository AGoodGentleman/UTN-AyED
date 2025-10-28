import random

def linear_search(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1

lista_0 = []
i = 0

while i < 10:
    lista_0.append(random.randint(0,100))
    i+=1

choice = int(input("Elija un numero del 0 al 100: "))
indice =  linear_search(lista_0,choice) 

if indice == -1:
    print("El numero no se ha encontrado en la lista.")
else: print(f"El numero {choice} esta la lista y se encuentra en el indice {indice} (posicion {indice+1}).")

print(lista_0)