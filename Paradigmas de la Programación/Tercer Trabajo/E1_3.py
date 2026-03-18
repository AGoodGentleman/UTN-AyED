def antes_despues(func):
    def wrapper():
        print("Antes de ejecutar la función...")
        func()
        print("Después de ejecutar la función...")
    return wrapper

@antes_despues
def hola_mundo():
    print("Hola mundo")

hola_mundo()