check = False

class Persona:
    def __init__(self, nombre= None, apellido= None, edad= 0, DNI= 0):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.DNI = DNI

    def mostrar(self):
        return f"Los datos de la persona son: {self.nombre} {self.apellido}, {self.edad} años, DNI número {self.DNI}."
    
    def mayor(self):
        check = False
        if self.edad >= 18:
            check = True
        else:
            check = False

        return f"{self.nombre} {self.apellido} es mayor de edad: {check}."
    
persona_1 = Persona("Luca Valentin","Blazquez", 18, 47798638)
persona_2 = Persona("Matías","Enrique", 17, 50123789)

print(persona_1.mostrar())

print(persona_1.mayor())

print(persona_2.mostrar())

print(persona_2.mayor())