frase = input("Ingrese una frase: ")

n_frase = ""

c = 0

for index in range (len(frase)):
    if frase[index] == " ":
        n_frase = frase[c:index]
        print(n_frase)
        index +=1
        c = index

n_frase = frase[c:index+1]
print(n_frase)