import os

my_list = []

full_list = []

found = False

def create(name,qty,price):
    
    with open("sales.txt", "a") as file:
        
        file.write(f"{name}, {qty}, {price}\n")

def consult():

    global file

    file = open("sales.txt", 'r')
    
    global my_list
    
    my_list = file.readlines()

    for element in my_list:
        print(element)

    file.close()

def check(name):

    global found

    found = False

    with open("sales.txt", "r") as file:
        lines = file.readlines()
        for element in lines:
            if name in element:
                found = True
                break
    return found

def update(name):
    consult()
    global my_list
    found = False
    for i in range(len(my_list)):
        if name in my_list[i]:
            change_1 = input("Ingrese el nuevo nombre: ")
            change_2 = input("Ingrese la nueva cantidad vendida: ")
            change_3 = input("Ingrese el nuevo precio: ")
            my_list[i] = f"{change_1}, {change_2}, {change_3}\n"
            found = True
            break
    if found:
        with open("sales.txt", 'w') as file:
            file.writelines(my_list)
    else:
        print("No se encontró el valor a actualizar.")
        
def eliminate(name):
    consult()
    global my_list
    found = False
    new_list = []
    for line in my_list:
        if name == line.split(",")[0].strip():
            found = True
        else:
            new_list.append(line)
    if found:
        my_list = new_list
        with open("sales.txt", 'w') as file:
            file.writelines(my_list)
    else:
        print("No se encontró el valor a eliminar.")

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

def sales():

    list_()

    money = 0

    for line_full in full_list:
        money += int(line_full[1]) * float(line_full[2])
    
    return money
            
def sales_p(name):

    list_()

    money = 0

    for line_full in full_list:
        if name == line_full[0]:
            money += int(line_full[1]) * float(line_full[2])
    
    return money

def exit_():
    os.remove("sales.txt")

####################################################

while True:
    stop = "No"
    print("Bienvenido a su terminal de productos.")
    print("")
    print("¿Qué desea hacer?")
    print("")
    print("1: Crear Lista," \
    "2: Añadir un producto," \
    "3: Consultar los productos actuales," \
    "4: Actualizar las ventas o el precio de un producto," \
    "5: Eliminar un producto," \
    "6: Calcular Ventas Totales," \
    "7: Calcular Ventas Individuales," \
    "" \
    "0: Salir (Eliminará el archivo)")
    choice = int(input(""))
    while stop != "Yes":
        if choice == 1:
            create(input("Ingrese el nombre de su producto: "),
            int(input("Ingrese la cantidad que se vendió de dicho producto: ")),
            float(input("Ingrese el precio de dicho producto: ")))
            stop = input("Si desea parar, escriba Yes, si no, escriba No: ")
        elif choice == 2:
            name = input("Ingrese el nombre del producto a añadir: ")
            qty = int(input("Ingrese la cantidad vendida: "))
            price = float(input("Ingrese el precio: "))
            my_list.append(f"{name}, {qty}, {price}\n")
            with open("sales.txt", 'a') as file:
                file.write(f"{name}, {qty}, {price}\n")
            stop = "Yes"
        elif choice == 3:
            print("Los productos actualmente en la base de datos son: ")
            print("")
            consult()
            stop = "Yes"
        elif choice == 4:
            search_for = input("Ingrese el producto a actualizar: ")
            check(search_for)
            if found == True:
                update(search_for)
            stop = "Yes"
        elif choice == 5: 
            search_for = input("Ingrese el producto a eliminar: ")
            check(search_for)
            if found == True:
                eliminate(search_for)
            stop = "Yes"
        elif choice == 6:
            print(f"Sus ventas totales son {sales()}.")
            stop = "Yes"
        elif choice == 7:
            search_for = input("Ingrese el producto a chequear ventas: ")
            check(search_for)
            if found == True:
                print(f"Sus ventas de este producto son: {sales_p(search_for)}.")
            stop = "Yes"
        elif choice == 0:
            exit_()
            break