frase = input("Ingrese una frase que tenga mas de 5 caracteres: ")

if len(frase) > 5:
    print(frase[0:3])
else:
    print("La frase que usted ha ingresado no tiene mas de 5 caracteres.")