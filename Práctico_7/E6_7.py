stop = False
keep_going = 1
lista_empleado = []
lista_salario = []

class Empleado:
    def __init__(self,nombre,horas_t=0.0,tarifa_h=0.0):
        self.nombre = nombre
        self.horas_t = horas_t
        self.tarifa_h = tarifa_h
    
    def calculo_s(self):
        self.salario = self.horas_t*self.tarifa_h
        return self.salario

    def __str__(self):
        return f"Nombre: {self.nombre}, Horas: {self.horas_t}, Tarifa: {self.tarifa_h}."
    
while stop == False:
    nombre = input("Ingrese el nombre de su empleado: ")
    horas_t = float(input("Ingrese las horas trabajadas por su empleado: "))
    tarifa_h = float(input("Ingrese la tarifa por hora de su empleado: "))
    empleado_g = Empleado(nombre,horas_t,tarifa_h)
    lista_empleado.append(empleado_g)
    lista_salario.append(f"El salario de {empleado_g.nombre} es {str(empleado_g.calculo_s())}")
    keep_going = int(input("Si desea seguir, ingrese 1. Si desea parar, ingrese 0: "))
    if keep_going == 0:
        stop = True

for element in lista_empleado:
    print(element)

for element in lista_salario:
    print(element)