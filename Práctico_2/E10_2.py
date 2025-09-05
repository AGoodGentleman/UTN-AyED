file = input("Ingrese un nombre de archivo: ")

new_file = ""

ext = len(file)

for index in range(len(file)):
    if file[index] == " ":
        new_file += "_"
    elif index < ext:
        new_file += file[index] # file = file + file[index]
    if file[index] == ".":
        ext = index

new_file = new_file + "#"*(len(file)-ext-1)

print(new_file)