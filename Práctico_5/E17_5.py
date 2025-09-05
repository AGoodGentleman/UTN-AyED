def position (word, char):
    index = 1
    pos = 0
    for element in word:
        if element == char:
            pos = index
            break
        index += 1
    if pos == 0:
        print("No existe dicha letra en la cadena ingresada.")
    else:
        return pos
    
x = str(input("Ingrese una cadena: "))

y = str(input("Ingrese una letra: "))

print(f"La primera vez que aparece su caracter en la cadena ingresada es {position(x,y)}")