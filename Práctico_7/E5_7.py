stop = False
keep_going = 1
lista_vehículo = []
lista_marca = []

class Vehiculo:
    def __init__(self,marca,modelo,patente,color):
        self.marca = marca
        self.modelo = modelo
        self.patente = patente
        self.color = color
        pass

    def __str__(self):
        return f"Marca: {self.marca}, Modelo: {self.modelo}, Patente: {self.patente}, Color: {self.color}."

while stop == False:
    marca = input("Ingrese la marca de su vehículo: ")
    modelo = input("Ingrese el modelo de su vehículo: ")
    patente = (input("Ingrese la patente de su vehículo: "))
    color = input("Ingrese el color de su vehículo: ")
    vehiculo_g = Vehiculo(marca,modelo,patente,color)
    lista_vehículo.append(vehiculo_g)
    lista_marca.append(vehiculo_g.marca)
    keep_going = int(input("Si desea seguir, ingrese 1. Si desea parar, ingrese 0: "))
    if keep_going == 0:
        stop = True

for element in lista_vehículo:
    print(element)

my_dict = {}

for element in lista_marca:
    if element in my_dict:
        my_dict[element] += 1
    else:
        my_dict[element] = 1

print(my_dict)