def cuadrante (x,y):
    if x > 0:
        if y > 0:
            print("El punto se encuentra en el cuadrante 1.")
        elif y < 0:
            print("El punto se encuentra en el cuadrante 4.")
        else:
            print("El punto es tangente al eje x entre los cuadrantes 1 y 4.")
    elif x < 0:
        if y > 0:
            print("El punto se encuentra en el cuadrante 2.")
        elif y < 0:
            print("El punto se encuentra en el cuadrante 3.")
        else:
            print("El punto es tangente al eje x entre los cuadrantes 2 y 3.")
    else:
        if y > 0:
            print("El punto es tangente al eje y entre los cuadrantes 1 y 2.")
        elif y < 0:
            print("El punto es tangente al eje y entre los cuadrantes 3 y 4.")
        else:
            print("El punto es el orígen (0,0).")

cuadrante(int(input("Ingrese su coordenada en x: ")), int(input("Ingrese su coordenada en y: ")))