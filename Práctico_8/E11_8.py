class Cola():
    def __init__(self):
        self.value = []
    def queue (self, nombre, hojas):
        self.value.append({"Nombre" : nombre, "Hojas" : hojas})
        return self.value
    def dequeue (self):
        self.value.pop(0)

printer = Cola()

option = None

while option != 0:
    option = int(input("Seleccione: 1, agregar archivos; 2, imprimir el primero; 0, salir: "))
    if option == 1:    
        nombre = input("Ingrese el nombre de su archivo: ")
        hojas = input("Ingrese la cantidad de hojas de su archivo: ")
        printer.queue(nombre, hojas)
    elif option == 2:
        print(f"Imprimiendo {printer.value[0] ['Nombre']}")
        printer.dequeue()
    elif option == 0:
        print("Hasta pronto.")
    else:
        print("Usted no ha seleccionado una opción válida, intentelo nuevamente.")
        pass