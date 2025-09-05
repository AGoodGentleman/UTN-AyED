import random

def create(name):
    file = open(f"{name}.txt", 'w')

    for i in range(250):
        file.write(f"{random.randint(1,100)}\n")

    file.close

create(input("Ingrese el nombre del archivo a crear: ")) #Creará un archivo con el nombre elegido