import random

def linear_search(lista, objetivo):
    counter = 0
    index_list = []
    for i in range(len(lista)):
        if lista[i] == objetivo:
            counter += 1
            index_list.append(i)
    if counter == 0:
        print(-1)
    else:
        print("Se ha encontrado el elemento en los siguientes indices: ")
        for j in range(len(index_list)):
            print(index_list[j],end=" ")

lista_0 = []
k = 0

while k < 3:
    lista_0.append(random.randint(0,10))
    lista_0.append(random.randint(0,10))
    lista_0.append(random.randint(0,10))
    k += 1

print(lista_0)
choice = int(input("Elija un numero del 0 al 10: "))

linear_search(lista_0,choice)