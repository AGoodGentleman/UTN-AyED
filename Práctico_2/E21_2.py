phrase = input("Ingrese una frase: ")

my_list = []

for index in range(len(phrase)):
    if phrase[index] == " ":
        continue
    else:
        my_list.append(phrase[index])

print(my_list)