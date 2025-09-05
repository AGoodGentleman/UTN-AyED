x = 3
def f():
    y = x + 1
    print(x)
    def g():
        x = 1
        print(y)
        print(x)
    g()
f()

#Imprimirá en órden: 3, 4, 1, ya que:
# x = 3 es global,
#luego y = x+1 se vuelve local en f(),
#luego x = 1 se vuelve local en g(),
#Por lo tanto, primero imprime 3 (print(x) y x globalmente 3)
#Aquí, y localmente se volverá 3 por lo que queda de f()
#luego 4 (print (y) con y = x+1 y x localmente 1)
#luego 1 (print(x) con x localmente 1)