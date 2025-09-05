name = ""

surname = ""

name_list =[]

surname_list=[]

while name != "Done":
    name = input("Ingrese los nombres a continuacion y cuando termine, escriba Done: ")
    if name != "Done":
        name_list.append(name)

while surname != "Done":
    surname = input("Ingrese los apellidos a continuacion y cuando termine, escriba Done: ")
    if surname != "Done":
        surname_list.append(surname)

print(name_list)

print(surname_list)