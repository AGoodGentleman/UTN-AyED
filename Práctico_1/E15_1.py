word1 = str(input("Ingrese una palabra: "))
word2 = str(input("Ingrese otra palabra: "))
if len(word1) > len(word2):
    print(f"{word1} tiene mayor longitud que {word2}")
elif len(word2) > len(word1):
    print(f"{word2} tiene mayor longitud que {word1}")
else:
    print("Ambas palabras tienen la misma longitud.")