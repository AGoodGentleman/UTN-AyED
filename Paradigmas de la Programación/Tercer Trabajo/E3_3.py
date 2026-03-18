def mayusculas(func):
    def wrapper():
        resultado = func()
        return resultado.upper()
    return wrapper

@mayusculas
def saludar():
    return "hola mundo"

print(saludar())