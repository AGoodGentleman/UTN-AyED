def linear_search(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1

lista_0 = ["María","Nushi","Jose","Wei","Yan","Ali","John","David","Li","Abdul","Ana","Ying","Michael","Juan","Anna"]
i = 0

choice = input("Ingrese un nombre: ")
indice =  linear_search(lista_0,choice) 

if indice == -1:
    print("El nombre no se ha encontrado en la lista (no se presentó).")
else: print(f"El nombre {choice} esta la lista y se encuentra en el indice {indice} (posicion {indice+1}) (sí se presentó).")

print(lista_0)