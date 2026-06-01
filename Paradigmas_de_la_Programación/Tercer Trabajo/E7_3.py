def validar_enteros(func):
    def wrapper(*args, **kwargs):

        for arg in args:
            if type(arg) != int:
                print("Error: todos los argumentos deben ser enteros")
                return

        for valor in kwargs.values():
            if type(valor) != int:
                print("Error: todos los argumentos deben ser enteros")
                return

        return func(*args, **kwargs)

    return wrapper

@validar_enteros
def sumar(a, b):
    return a + b

@validar_enteros
def mostrar_numero(n):
    print(f"Número: {n}")

print(sumar(3, 5))