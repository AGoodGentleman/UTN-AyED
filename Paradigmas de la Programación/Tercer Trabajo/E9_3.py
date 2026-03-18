# =========================
# @staticmethod
# =========================
# Un método estático es una función dentro de una clase que no recibe ni la instancia (self) ni la clase (cls). 
# Se usa cuando la función no depende de datos de la clase ni del objeto.

class Calculadora:

    @staticmethod
    def sumar(a, b):
        return a + b

# Ejemplo de uso
resultado = Calculadora.sumar(3, 5)
print("Resultado staticmethod:", resultado)

# =========================
# @classmethod
# =========================
# Un método de clase recibe la clase como primer parámetro (cls) y permite acceder o modificar atributos de clase. 
# Se usa también como constructor alternativo.

class Persona:
    cantidad = 0

    def __init__(self, nombre):
        self.nombre = nombre
        Persona.cantidad += 1

    @classmethod
    def total_personas(cls):
        return cls.cantidad

# Ejemplo de uso
p1 = Persona("Valen")
p2 = Persona("Vicky")
print("Total personas:", Persona.total_personas())

# =========================
# @property
# =========================
# Permite usar un método como si fuera un atributo. 
# Se utiliza para controlar el acceso a los datos (por ejemplo, validaciones o transformaciones).

class PersonaProp:

    def __init__(self, nombre):
        self._nombre = nombre

    @property
    def nombre(self):
        return self._nombre.upper()

# Ejemplo de uso
p = PersonaProp("valen")
print("Nombre con property:", p.nombre)