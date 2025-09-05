frase = input("Ingrese una frase: ")

for char in frase:
    if char == "a":
        print("4", end="")
    elif char == "e":
        print("3", end="")
    else: 
        print(char, end="")