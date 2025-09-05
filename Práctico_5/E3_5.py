frase = "Hola"

def f():
    frase = "Es un lindo dia"
    print(frase)

f()

#El código imprimirá "Es un lindo día" ya que si bien tengo una frase en global
#Cuando la uso dentro de la función, la redefino para local y no da el mismo error que en el ejercicio 2.

#La primer frase (hola) es la variable que tiene alcance global y persiste a través de todo el algoritmo
#La segunda frase (es un lindo día) es la variable que tiene alcance local y desaparece luego de la ejecución de la función.