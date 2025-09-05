#Sin lista:

phrase = input("Ingrese una frase: ")

new_word = ""

new_phrase = ""

counter = 0

for index in range(len(phrase)):
    if phrase[index] != " ":
        new_word = new_word + phrase[index]
    elif phrase[index] == " ":
         new_phrase = new_phrase + new_word + " "
         new_word = ""
         counter += 1
else:
    new_phrase = new_phrase + new_word
    counter += 1

print(new_phrase)

print(counter)

#Con lista:

my_list = []

phrase = input("Ingrese una frase: ")

new_word = ""

counter = 0

for index in range(len(phrase)):
    if phrase[index] != " ":
        new_word = new_word + phrase[index]
    elif phrase[index] == " ":
         my_list.append(new_word)
         new_word = ""
         counter += 1
else:
    my_list.append(new_word)
    counter += 1

for element in my_list:
    print(element, end=" ")

print("")

print(counter)