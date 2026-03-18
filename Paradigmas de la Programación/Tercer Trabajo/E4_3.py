def repetir(n):
    def decorador(func):
        def wrapper():
            for i in range(n):
                func()
        return wrapper
    return decorador

limit = int(input("Ingrese la cantidad de hola mundos: "))

@repetir(limit)
def saludar():
    print("Hola Mundo")

saludar()