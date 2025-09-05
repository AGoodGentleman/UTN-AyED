array = []

new_array = []

for i in range(5):
    array.append(float(input("Ingrese 5 numeros, uno por vez: ")))

j = len(array) - 1

while j >= 0:
    new_array.append(array[j])
    j -=1

print(new_array)