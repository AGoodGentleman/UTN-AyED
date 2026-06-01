def requiere_rol(rol_requerido):
    def decorador(func):
        def wrapper(*args, **kwargs):
            if rol_requerido == "admin":
                return func(*args, **kwargs)
            else:
                print("Acceso denegado: se requiere rol admin")
        return wrapper
    return decorador

@requiere_rol("admin")
def funcion_critica():
    print("Ejecutando acción crítica...")

@requiere_rol("usuario")
def funcion_normal():
    print("Esto no debería ejecutarse si no es admin")

funcion_critica()
funcion_normal()