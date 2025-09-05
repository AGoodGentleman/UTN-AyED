phrase = input("Ingrese una frase: ")

my_list = []

word = ""

for index in range(len(phrase)):
    if phrase[index] != " ":
        word = word + phrase[index]
    elif phrase[index] == " " and index != len(phrase):
        my_list.append(word)
        word = ""

my_list.append(word)

print(my_list)