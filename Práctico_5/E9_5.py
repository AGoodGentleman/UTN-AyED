def appearances (word, letter):
    c = 0
    for i in word:
        if i == letter:
            c += 1
    print(f"La cantidad de veces que {letter} aparece en {word} es {c}.")

appearances (input("Ingrese una palabra (en minúsculas): "), input("Ingrese una letra: "))