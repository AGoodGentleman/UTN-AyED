name_list = []

surname_list = []

word = ""

user_input = ""

while user_input != "Done":
    user_input = input("Ingrese el primer nombre y primer apellido de cada persona a continuación. Cuando esté listo, escriba Done: ")
    
    if user_input == "Done":
        break

    word = ""
    for index in range(len(user_input)):
        if user_input[index] != " ":
            word = word + user_input[index]
        else:
            name_list.append(word)
            word = ""
            break

    index += 1
    word = ""
    while index < len(user_input):
        word = word + user_input[index]
        index += 1
    surname_list.append(word)

print(name_list)

print(surname_list)