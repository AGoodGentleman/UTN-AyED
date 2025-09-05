file_name = "archivo_1.txt"

file = open(file_name, "a")

word = input("Ingrese la primer palabra a escribir: ")

counter = 0

while word != "parar":

    file.write(f"{word}\n")
    word = input("Ingrese la siguiente a escribir (parar para parar): ")
    counter += 1

file = open(file_name, "r")

print(file.read())

print(f"Había {counter} palabras.")

file.close()