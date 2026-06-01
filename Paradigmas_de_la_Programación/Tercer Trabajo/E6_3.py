from datetime import datetime

def registrar_llamada(func):
    def wrapper(*args, **kwargs):

        ahora = datetime.now()
        marca_tiempo = ahora.strftime("%Y-%m-%d %H:%M:%S")

        with open("log.txt", "a") as archivo:
            archivo.write(f"{func.__name__} fue llamada en {marca_tiempo}\n")

        return func(*args, **kwargs)

    return wrapper

@registrar_llamada
def saludar(nombre):
    print(f"Hola, {nombre}")

@registrar_llamada
def sumar(a, b):
    return a + b

saludar("Valen")
print(sumar(3, 5))