frase = input("Ingrese una frase: ")

letter = input("Seleccione una letra: ")

c = 0

for char in frase:
    if letter == char:
        c+=1

print(f"Su letra aparece {c} veces.")

frase = input("Ingrese otra frase: ")

letter = input("Seleccione otra letra: ")

d = 0

for index in frase:
    if letter == index:
        d+=1

print(f"Su letra aparece {d} veces.")