def insertion_sort(lista):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and ((len(lista[j]) > len(actual))):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista

nombres = ["Juan", "Mariana", "Pedro", "Ana", "Guadalupe", "Luis", "Cecilia", "Tomás", "Rosa", "Ignacio"]

print(insertion_sort(nombres))