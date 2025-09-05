word = str(input("Ingrese una palabra: "))
if len(word) > 5:
    lenght = len(word)
    print(f"Su palabra tiene {lenght} caracteres.")
else:
    print("Su palabra tiene menos menos o igual a 5 caracteres.")