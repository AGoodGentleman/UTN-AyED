import os

my_list = []

full_list = []

found = False

counter = 0

def create(name,num,email):

    with open("agenda.txt", "a") as file:

        file.write(f"{name}, {num}, {email}\n")

def consult():

    global file

    global counter

    file = open("agenda.txt", 'r')
    
    global my_list
    
    my_list = file.readlines()

    for element in my_list:
        print(element)
        counter += 1

    file.close()

def count():

    global file

    global counter

    counter = 0

    file = open("agenda.txt", 'r')
    
    global my_list
    
    my_list = file.readlines()

    for element in my_list:
        counter += 1

    file.close()

def check(name):

    global found

    found = False

    with open("agenda.txt", "r") as file:
        lines = file.readlines()
        for element in lines:
            if name in element:
                found = True
                break
    return found

def update(name):

    global my_list

    change_1 = input("Ingrese el nuevo nombre: ")
    change_2 = input("Ingrese nuevo numero: ")
    change_3 = input("Ingrese nuevo email: ")

    gtg = False

    for i in range(len(my_list)):
        if name in my_list[i]:
            my_list[i] = f"{change_1}, {change_2}, {change_3}\n"
            with open("agenda.txt", "w") as file:
                file.writelines(my_list)
            print("Contacto actualizado.")
            gtg = True
            break
    if not gtg:
        print("No se encontró el valor a actualizar.")
    
        
def eliminate(name):

    global my_list

    gtg = False

    for index in range(len(my_list)):
        if name in my_list[index]:
            my_list.pop(index)
            gtg = True
    if not gtg:
        print("No se encontró el valor a actualizar.")

def list_():
    
    global my_list

    global full_list

    full_list = []

    for element in my_list:
        new_element = []
        head = 0
        for i in range(len(element)):
            if element[i] == ',':
                 new_element.append(element[head:i])
                 head = i+1
        full_list.append(new_element)

def exit_():
    os.remove("agenda.txt")

####################################################

while True:
    stop = "No"
    print("Bienvenido a su agenda telefonica.")
    print("")
    print("¿Qué desea hacer?")
    print("")
    print("1: Crear Lista," \
    "2: Añadir un contacto," \
    "3: Consultar los contactos actuales," \
    "4: Actualizar el numero o email de un contacto," \
    "5: Eliminar un contacto," \
    "6: Buscar un contacto," \
    "7: Contar contactos totales," \
    "" \
    "0: Salir (Eliminará el archivo)")
    choice = int(input(""))
    while stop != "Yes":
        if choice == 1:
            create(input("Ingrese el nombre de su contacto: "),
            int(input("Ingrese el numero de telefono de su contacto: ")),
            input("Ingrese el email de su contacto: "))
            stop = input("Si desea parar, escriba Yes, si no, escriba No: ")
        elif choice == 2:
            name = input("Ingrese el nombre del contacto a añadir: ")
            num = input("Ingrese el numero de telefono a añadir: ")
            email = input("Ingrese el email a añadir: ")
            nuevo_contacto = f"{name}, {num}, {email}\n"
            my_list.append(nuevo_contacto)
            file = open("agenda.txt", "a")
            file.write(nuevo_contacto)
            file.close()
        elif choice == 3:
            print("Los contactos actualmente en la base de datos son: ")
            print("")
            consult()
            stop = "Yes"
        elif choice == 4:
            search_for = input("Ingrese el contacto a actualizar: ")
            check(search_for)
            if found == True:
                update(search_for)
            stop = "Yes"
        elif choice == 5: 
            search_for = input("Ingrese el contacto a eliminar: ")
            check(search_for)
            if found == True:
                eliminate(search_for)
            stop = "Yes"
        elif choice == 6:
            search_for = input("Ingrese el contacto a buscar: ")
            check(search_for)
            if found == True:
                for element in my_list:
                    if search_for in element:
                        print(f"Contacto encontrado: {element.strip()}")
                        break
            else:
                print("Contacto no encontrado.")
            stop = "Yes"
        elif choice == 7:
            count()
            print(f"Hay {counter} contactos en su agenda.")
            stop = "Yes"
        elif choice == 0:
            exit_()
            break