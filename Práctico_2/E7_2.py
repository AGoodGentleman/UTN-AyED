frase = input("Ingrese una frase: ")

for index in range (0,len(frase),2):
    print(frase[index])

for index in range (len(frase)):
    if index%2 == 0:
        print(frase[index])