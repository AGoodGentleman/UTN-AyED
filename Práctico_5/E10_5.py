d = 0

def appearances (word, letter):
    c = 0
    for i in word:
        if i == letter:
            c += 1
    global d
    d =  d + c

u_letter = input("Ingrese una letra: ")

for j in range (10):
    u_word = input("Ingrese una palabra: ")
    appearances(u_word, u_letter)
    print (u_word)

print(f"La cantidad de veces que {u_letter} aparece en las 10 palabras es {d}.")