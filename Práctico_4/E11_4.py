min = 1

max = 33

array = [33, 11, 20, 2, 15, 1, 12, 11, 8, 14, 10]

sum = 0

average = 0

for element in array:
    if element >= max:
        max = element
    elif element <= min:
        min = element

array.remove(min)

print(f"La nota eliminada fue {min}.")

for element in array:
    sum = sum + element

average = sum/len(array)

print(f"El promedio de notas sin contar {min} es {average}.")