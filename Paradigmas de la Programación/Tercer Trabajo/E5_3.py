def verificar_password(func):
    def wrapper():
        password = input("Ingrese la contraseña: ")
        if password == "1234":
            return func()
        else:
            print("Contraseña incorrecta. Acceso denegado.")
    return wrapper

@verificar_password
def funcion_secreta():
    print("Acceso concedido. Ejecutando función...")

funcion_secreta()