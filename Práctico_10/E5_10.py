import array

def insertion_sort_array(arr):
    for i in range(1, len(arr)):
        actual = arr[i]
        j = i - 1
        # Mueve los elementos mayores hacia la derecha
        while j >= 0 and arr[j] > actual:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = actual
    return arr

#La principal diferencia es que se usa array.array para definir el array y que no se pueden mezclar los tipos de datos.