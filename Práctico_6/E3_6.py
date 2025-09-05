file_name = "colores.txt"

file = open(file_name, "a")

for i in range(5):
    color = input("Ingrese un color: ")
    file.write(f"{color}\n")
    
file = open(file_name, "r")

print(file.read())

file.close()