even = False

odd = False

def EorO (num):
    
    global even
    global odd

    if num % 2 == 0:
        even = True
        odd = False
    elif num % 2 == 1:
        odd = True
        even = False
    else:
        print("Su numero no es par ni impar, porque no es entero.")

    if even == True:
        print("Su numero es Par.")
    elif odd == True:
        print("Su numero es Impar.")

EorO(float(input("Ingrese un numero: ")))