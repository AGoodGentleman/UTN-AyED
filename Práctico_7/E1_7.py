class Alumno:
    def __init__(self,name,grade):
        self.name = name
        self.grade = grade

    def __str__(self):
        return f"Nombre: {self.name} y Nota: {self.grade}"
    
    def passed(self):
        if self.grade >= 6:
            return f"{self.name} aprobó con {self.grade}."
        else:
            return f"{self.name} no aprobó con {self.grade}."
        
option = int(input("Para ingresar alumnos, ingrese 1, para ver los que ya tiene, ingrese 2 y para salir ingrese 0: "))

name = ""

grade = 0

aula = []

while option != 0:
    if option == 1:
        name = str(input("Ingrese el nombre del alumno: "))
        grade = float(input("Ingrese la nota del alumno: "))
        aula.append(Alumno(name, grade))
    elif option == 2:
        for alumno in aula:
            print(alumno.passed())

    option = int(input("Para ingresar alumnos, ingrese 1, para ver los que ya tiene, ingrese 2 y para salir ingrese 0: "))