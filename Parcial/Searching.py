def linear_search(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1

#Ejemplo

datos = [3, 5, 2, 9, 1]
print(linear_search(datos, 9))

def binary_search(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1

#Ejemplo

datos = [1, 3, 5, 7, 9, 11]
print(binary_search(datos, 7))

def interpolation_search(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha and lista[izquierda] <= objetivo <= lista[derecha]:
        pos = izquierda + int(
            ((objetivo - lista[izquierda]) * (derecha - izquierda)) /
            (lista[derecha] - lista[izquierda])
        )
        if lista[pos] == objetivo:
            return pos
        elif lista[pos] < objetivo:
            izquierda = pos + 1
        else:
            derecha = pos - 1
    return -1

def exponential_search(lista, objetivo):
    if lista[0] == objetivo:
        return 0

    i = 1
    while i < len(lista) and lista[i] <= objetivo:
        i *= 2

    izquierda = i // 2
    derecha = min(i, len(lista) - 1)
    return binary_search(lista[izquierda:derecha+1], objetivo)