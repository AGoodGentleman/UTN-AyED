def cuadrado (num):
    name = "Valentin"
    surname = "Blazquez"
    age = 18
    print (f"Las variables locales son {locals()}.") #Se imprime "{'num': el numero en cuestión}".
    #Si añado extras, como lo añadido, se imprimirá: "{'num': el numero en cuestión, 'name':'Valentin', 'surname':'Blazquez', 'age': 18}".
    print (f"El cuadrado es {num * num}.")

cuadrado(int(input("Ingrese su numero: ")))