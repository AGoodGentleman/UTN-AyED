def insertion_sort(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        #Mueve los elementos mayores hacia la derecha
        while j >= 0 and lista[j] > actual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista

def insertion_sort_reversed(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        #Mueve los elementos mayores hacia la derecha
        while j >= 0 and lista[j] < actual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista

grades_list = []

i = 0

while i < 10:
    grades_list.append(float(input("Ingrese la próxima nota: ")))
    i += 1

print(f"Menor a mayor: {insertion_sort(grades_list)}")
print(f"Mayor a menor: {insertion_sort_reversed(grades_list)}")