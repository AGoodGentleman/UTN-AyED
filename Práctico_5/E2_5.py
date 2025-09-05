n = 5

def cuadrado():
    global n
    
    # a) Mostrar el valor de n al cuadrado
    print("a) n al cuadrado:", n * n)  # Leer n global -> OK

    # b) Intentar modificar n sin declarar 'global' (esto daría error si se descomenta)
    # n = n + 1  # Esto lanzaría un error: UnboundLocalError

    # c) Para modificar n correctamente, usamos 'global'
    n = n + 1  # Modifica la variable global
    print("c) n modificado dentro de la función:", n)


# Mostrar valor inicial
print("Valor inicial de n:", n)

# Llamar a la función
cuadrado()

# Ver valor final de n (modificado por la función)
print("Valor final de n fuera de la función:", n)